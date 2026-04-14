import daemon


def main() -> None:
    worker = daemon.DistributedWorkerDaemon(geo_region="europe-west1")
    worker.start()


if __name__ == "__main__":
    main()
