# Extracted from: C:\DEV\PyAgent\.external\AEnvironment\api-service\scripts\perf.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import asyncio
import logging
import statistics
import time
import traceback
from collections import defaultdict
from datetime import datetime

import aiohttp

logging.basicConfig(level=logging.INFO)


class LoadTester:
    def __init__(
        self,
        host,
        concurrency,
        interval,
        execute_duration=0,
        duration=None,
        total_count=None,
    ):
        self.host = host.rstrip("/")  # Remove trailing slash
        self.concurrency = concurrency
        self.interval = interval
        self.execute_duration = execute_duration  # Simulated execution time for each request
        self.duration = duration
        self.total_count = total_count

        # Statistics data
        self.stats = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0, "times": []})

        # Instance ID list (for cleanup)
        self.instance_id_list = []
        self.instance_id_lock = asyncio.Lock()  # Protect concurrent access to instance_id_list

        # Test end flag
        self.start_time = None
        self.end_time = None
        self.request_counter = 0  # Global request counter
        self.lock = asyncio.Lock()  # Protect counter

    async def make_get_request(self, session, request_id):
        """Send GET request"""
        url = f"{self.host}/env-instance/{request_id}"
        start_time = time.time()
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                await response.text()  # Read response content
                elapsed = time.time() - start_time
                self.stats["GET"]["total"] += 1
                if response.status == 200:
                    self.stats["GET"]["success"] += 1
                else:
                    self.stats["GET"]["failed"] += 1
                self.stats["GET"]["times"].append(elapsed)
                return response.status
        except Exception as e:
            elapsed = time.time() - start_time
            self.stats["GET"]["total"] += 1
            self.stats["GET"]["failed"] += 1
            self.stats["GET"]["times"].append(elapsed)
            return str(e)

    async def make_post_request(self, session, request_id):
        """Send POST request"""
        url = f"{self.host}/env-instance"
        data = {
            "name": "perf-test-" + request_id,
            "description": "perf-test",
            "envName": "search@1.0.0",
            "labels": {"test": "test"},
        }
        start_time = time.time()
        try:
            async with session.post(url, json=data, timeout=aiohttp.ClientTimeout(total=30)) as response:
                body = await response.json()
                elapsed = time.time() - start_time
                self.stats["POST"]["total"] += 1
                if response.status == 200 or response.status == 201:
                    self.stats["POST"]["success"] += 1
                    instance_id = body.get("data", {}).get("id", "")
                    if instance_id:
                        async with self.instance_id_lock:
                            self.instance_id_list.append(instance_id)
                        return instance_id
                else:
                    self.stats["POST"]["failed"] += 1
                    logging.error(f"POST request failed: {response.status}, {body}")
                self.stats["POST"]["times"].append(elapsed)
                return ""
        except Exception as e:
            print(f"POST request failed: {e}")
            elapsed = time.time() - start_time
            self.stats["POST"]["total"] += 1
            self.stats["POST"]["failed"] += 1
            self.stats["POST"]["times"].append(elapsed)
            return ""

    async def make_delete_request(self, session, request_id):
        """Send DELETE request"""
        url = f"{self.host}/env-instance/{request_id}"
        start_time = time.time()
        try:
            async with session.delete(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                response_text = await response.text()
                elapsed = time.time() - start_time
                self.stats["DELETE"]["total"] += 1
                if response.status == 200 or response.status == 204:
                    self.stats["DELETE"]["success"] += 1
                    # Remove instance_id from list after successful deletion
                    async with self.instance_id_lock:
                        if request_id in self.instance_id_list:
                            self.instance_id_list.remove(request_id)
                else:
                    self.stats["DELETE"]["failed"] += 1
                    logging.error(f"DELETE request failed: {response.status}, {response_text}")
                self.stats["DELETE"]["times"].append(elapsed)
                return response.status
        except Exception as e:
            elapsed = time.time() - start_time
            self.stats["DELETE"]["total"] += 1
            self.stats["DELETE"]["failed"] += 1
            self.stats["DELETE"]["times"].append(elapsed)
            return str(e)

    async def should_continue(self):
        """Check if should continue execution"""
        async with self.lock:
            if self.total_count is not None:
                # Judge by total count
                return self.request_counter < self.total_count
            elif self.duration is not None:
                # Judge by time
                return time.time() - self.start_time < self.duration
            return True

    async def increment_counter(self):
        """Increment request counter"""
        async with self.lock:
            self.request_counter += 1
            return self.request_counter

    async def single_request_cycle(self, session, worker_id, cycle_id):
        """Single request cycle - Execute POST->GET->DELETE in order, sleep execute_duration seconds after each request"""
        request_id = f"{worker_id}_{cycle_id}"

        # 1. Execute POST request first
        instance_id = await self.make_post_request(session, request_id)

        if instance_id:
            # 2. Execute GET request next
            await self.make_get_request(session, instance_id)

            # Simulate request processing time
            if self.execute_duration > 0:
                await asyncio.sleep(self.execute_duration)

            # 3. Execute DELETE request last
            await self.make_delete_request(session, instance_id)

    async def worker(self, worker_id):
        """Worker coroutine - Execute concurrency request cycles per second, then sleep interval seconds"""
        async with aiohttp.ClientSession() as session:
            cycle_count = 0
            while await self.should_continue():
                cycle_count += 1

                # Execute concurrency request cycles per second
                tasks = []
                for i in range(self.concurrency):
                    # Check if should continue
                    if not await self.should_continue():
                        break

                    # Increment global counter
                    current_count = await self.increment_counter()
                    if self.total_count is not None and current_count > self.total_count:
                        break

                    task = self.single_request_cycle(session, worker_id, f"{cycle_count}_{i}")
                    tasks.append(task)

                if tasks:
                    # Execute all request cycles concurrently
                    asyncio.gather(*tasks, return_exceptions=True)

                # If there's still time and haven't reached total count limit, sleep interval seconds
                if await self.should_continue():
                    if self.total_count is None or (await self.increment_counter() - 1) < self.total_count:
                        await asyncio.sleep(self.interval)

    async def cleanup_remaining_instances(self):
        """Clean up remaining instances in instance_id_list"""
        if not self.instance_id_list:
            logging.info("No cleanup needed: no remaining instance_id")
            return

        logging.info(f"Starting cleanup of {len(self.instance_id_list)} remaining instances...")
        async with aiohttp.ClientSession() as session:
            tasks = [self.make_delete_request(session, inst_id) for inst_id in self.instance_id_list]
            await asyncio.gather(*tasks, return_exceptions=True)
        logging.info(f"Cleanup completed, processed {len(self.instance_id_list)} instances.")

    async def run_test(self):
        """Run load test"""
        print("Starting load test...")
        print(f"Target host: {self.host}")
        print(f"Concurrency per second: {self.concurrency}")
        print(f"Execution interval: {self.interval} seconds")
        if self.execute_duration > 0:
            print(f"Simulated execution time per request: {self.execute_duration} seconds")

        if self.total_count is not None:
            print(f"Total execution count: {self.total_count}")
            print("(Each cycle contains POST->GET->DELETE 3 requests, actual total requests = count × 3)")
        else:
            print(f"Duration: {self.duration} seconds")

        print("Request order: POST -> GET -> DELETE")
        print("-" * 50)

        self.start_time = time.time()

        # Create single worker task (use one worker to control overall pace)
        await self.worker(0)
        # Wait for last request to complete
        await asyncio.sleep(self.execute_duration)

        self.end_time = time.time()
        actual_duration = self.end_time - self.start_time

        print(f"Load test completed! Executed {self.request_counter} cycles, took {actual_duration:.2f} seconds")

        # After load test ends, clean up remaining instances
        await self.cleanup_remaining_instances()

    def calculate_percentile(self, times, percentile):
        """Calculate percentile"""
        if not times:
            return 0.0
        sorted_times = sorted(times)
        index = int(len(sorted_times) * percentile / 100)
        if index >= len(sorted_times):
            index = len(sorted_times) - 1
        return sorted_times[index]

    def generate_report(self):
        """Generate load test report"""
        total_duration = self.end_time - self.start_time if self.end_time else 0
        total_requests = sum(stat["total"] for stat in self.stats.values())
        total_success = sum(stat["success"] for stat in self.stats.values())
        total_failed = sum(stat["failed"] for stat in self.stats.values())

        print("\n" + "=" * 100)
        print("Load Test Report")
        print("=" * 100)

        # First line: Load test parameters
        if self.total_count is not None:
            print(
                f"Load test parameters: host={self.host}, concurrency={self.concurrency}, interval={self.interval}s, execute_duration={self.execute_duration}s, total_count={self.total_count}"
            )
        else:
            print(
                f"Load test parameters: host={self.host}, concurrency={self.concurrency}, interval={self.interval}s, execute_duration={self.execute_duration}s, duration={self.duration}s"
            )

        print("Request order: POST -> GET -> DELETE")
        print(f"Load test start time: {datetime.fromtimestamp(self.start_time) if self.start_time else 'N/A'}")
        print(f"Load test end time: {datetime.fromtimestamp(self.end_time) if self.end_time else 'N/A'}")
        print(f"Actual load test duration: {total_duration:.2f} seconds")
        print(f"Actual execution cycles: {self.request_counter}")
        print(f"Actual total requests: {total_requests} (cycles × 3)")
        print()

        # Statistics grouped by request type
        print(
            f"{'Request Type':<10} {'Total':<8} {'Success':<8} {'Failed':<8} {'Success Rate':<10} {'Avg Time':<12} {'Max Time':<12} {'P50 Time':<12}"
        )
        print("-" * 90)

        for method in ["POST", "GET", "DELETE"]:  # Display in execution order
            stat = self.stats[method]
            if stat["total"] > 0:
                success_rate = (stat["success"] / stat["total"]) * 100 if stat["total"] > 0 else 0
                avg_time = statistics.mean(stat["times"]) if stat["times"] else 0
                max_time = max(stat["times"]) if stat["times"] else 0
                p50_time = self.calculate_percentile(stat["times"], 50) if stat["times"] else 0
                print(
                    f"{method:<10} {stat['total']:<8} {stat['success']:<8} {stat['failed']:<8} {success_rate:.2f}%{'':<6} {avg_time:.4f}{'':<4} {max_time:.4f}{'':<4} {p50_time:.4f}"
                )
            else:
                print(f"{method:<10} {0:<8} {0:<8} {0:<8} {0.00}%{'':<6} {0.0000}{'':<4} {0.0000}{'':<4} {0.0000}")

        print("-" * 90)
        # Calculate overall statistics
        all_times = []
        for stat in self.stats.values():
            all_times.extend(stat["times"])

        overall_avg = statistics.mean(all_times) if all_times else 0
        overall_max = max(all_times) if all_times else 0
        overall_p50 = self.calculate_percentile(all_times, 50) if all_times else 0

        print(
            f"{'Total':<10} {total_requests:<8} {total_success:<8} {total_failed:<8} {(total_success / total_requests * 100) if total_requests > 0 else 0:.2f}%{'':<6} {overall_avg:.4f}{'':<4} {overall_max:.4f}{'':<4} {overall_p50:.4f}"
        )

        print("\nDetailed Statistics:")
        print(f"Execution cycles: {self.request_counter}")
        print(f"Total requests: {total_requests} (cycles × 3)")
        print(f"Successful requests: {total_success}")
        print(f"Failed requests: {total_failed}")
        print(f"Overall success rate: {(total_success / total_requests * 100) if total_requests > 0 else 0:.2f}%")
        print(f"Total duration: {total_duration:.2f} seconds")
        if total_duration > 0:
            print(f"Average QPS: {total_requests / total_duration:.2f}")
            print(f"Average cycles/second: {self.request_counter / total_duration:.2f}")


def main():
    parser = argparse.ArgumentParser(description="HTTP API load testing tool")
    parser.add_argument(
        "--host",
        required=True,
        help="Target host address (e.g., http://localhost:8080)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Concurrent requests per second (default: 10)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Execution interval time in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--execute-duration",
        type=float,
        default=0,
        help="Simulated execution time per request in seconds (default: 0)",
    )

    # Mutually exclusive parameter group: duration and total_count
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--duration", type=int, help="Load test duration in seconds")
    group.add_argument("--total-count", type=int, help="Total execution count (cycles)")

    args = parser.parse_args()

    # Parameter validation
    if args.concurrency <= 0:
        print("Error: Concurrency must be greater than 0")
        return

    if args.interval < 0:
        print("Error: Interval time cannot be negative")
        return

    if args.execute_duration < 0:
        print("Error: Execution duration cannot be negative")
        return

    if args.duration is not None and args.duration <= 0:
        print("Error: Load test duration must be greater than 0")
        return

    if args.total_count is not None and args.total_count <= 0:
        print("Error: Total execution count must be greater than 0")
        return

    # Run load test
    tester = LoadTester(
        host=args.host,
        concurrency=args.concurrency,
        interval=args.interval,
        execute_duration=args.execute_duration,
        duration=args.duration,
        total_count=args.total_count,
    )

    try:
        asyncio.run(tester.run_test())
        tester.generate_report()
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user")
        # Force cleanup of remaining instances
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(tester.cleanup_remaining_instances())
    except Exception as e:
        print(f"Error occurred during load test: {e}, {traceback.format_exc()}")
        # Also try to cleanup after error
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
        loop.run_until_complete(tester.cleanup_remaining_instances())


if __name__ == "__main__":
    main()
