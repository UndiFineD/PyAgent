# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\chocomintx.py\xiaohongshutools.py\scripts.py\request.py\web.py\apis.py\user_b3c83a9c73af.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\request\web\apis\user.py

from typing import TYPE_CHECKING

import aiohttp

if TYPE_CHECKING:
    from request.web.xhs_session import XHS_Session  # 仅类型检查时导入


class User:
    def __init__(self, session: "XHS_Session"):
        self.session = session  # 保存会话引用

    # 关注用户

    async def follow_user(self, target_user_id: str) -> aiohttp.ClientResponse:
        """关注用户

        Args:

            target_user_id: 目标用户ID

        Returns:

            点赞结果

        """

        url = "https://edith.xiaohongshu.com/api/sns/web/v1/user/follow"

        data = {"target_user_id": target_user_id}

        return await self.session.request(method="post", url=url, data=data)
