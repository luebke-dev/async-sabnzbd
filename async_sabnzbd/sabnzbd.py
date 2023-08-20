import httpx


class Sabnzbd:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        client: httpx.AsyncClient | None = httpx.AsyncClient(),
    ) -> None:
        self.client = client
        self.api_key = api_key
        self.base_url = base_url

    async def _request(
        self, sabnzbd_method: str, method: str = "GET", params: dict | None = None
    ):
        if params is None:
            params = {}
        params = {k: v for k, v in params.items() if v is not None}
        response = await self.client.request(
            method=method,
            url=f"{self.base_url}/sabnzbd/api",
            params={
                "apikey": self.api_key,
                "mode": sabnzbd_method,
                "output": "json",
                **params,
            },
        )
        data = response.json()
        return data

    async def change_complete_action(self, action: str):
        data = await self._request(
            sabnzbd_method="change_complete_action", params={"value": action}
        )
        return data

    async def sort_queue(self, key: str, direction: str):
        data = await self._request(
            sabnzbd_method="queue",
            params={"name": "sort", "sort": key, "direction": direction},
        )
        return data

    async def queue(
        self,
        start: int | None = None,
        limit: int | None = None,
        category: str | None = None,
        priority: int | None = None,
        search: str | None = None,
        nzo_ids: str | None = None,
    ):
        data = await self._request(
            sabnzbd_method="queue",
            params={
                "start": start,
                "limit": limit,
                "category": category,
                "priority": priority,
                "search": search,
                "nzo_ids": nzo_ids,
            },
        )
        return data["queue"]["slots"]

    async def get_files(self, nzo_id: str):
        data = await self._request(sabnzbd_method="get_files", params={"value": nzo_id})
        return data["files"]

    async def server_stats(self):
        data = await self._request(sabnzbd_method="server_stats")
        return data

    async def delete_job(self, nzo_id: str | list[str]):
        data = await self._request(
            sabnzbd_method="queue",
            params={
                "name": "delete",
                "value": nzo_id if isinstance(nzo_id, str) else ",".join(nzo_id),
            },
        )
        return data["status"]

    async def pause_job(self, nzo_id: str):
        data = await self._request(
            sabnzbd_method="queue", params={"name": "pause", "value": nzo_id}
        )
        return data

    async def purge_queue(
        self, search: str | None = None, delete_files: bool | None = None
    ):
        data = await self._request(
            sabnzbd_method="queue", params={"search": search, "del_files": delete_files}
        )
        return data

    async def resume_job(self, nzo_id: str):
        data = await self._request(
            sabnzbd_method="queue", params={"name": "resume", "value": nzo_id}
        )
        return data

    async def resume_queue(self):
        data = await self._request(sabnzbd_method="resume")
        return data["status"]

    async def pause_queue(self):
        data = await self._request(sabnzbd_method="pause")
        return data["status"]

    async def change_job_name(
        self, nzo_id: str, new_name: str | None = None, new_password: str | None = None
    ):
        data = await self._request(
            sabnzbd_method="queue",
            params={
                "name": "rename",
                "value": nzo_id,
                "value2": new_name,
                "value3": new_password,
            },
        )

        return data

    async def change_job_priority(self, nzo_id: str, priority: int):
        data = await self._request(
            sabnzbd_method="queue",
            params={
                "name": "priority",
                "value": nzo_id,
                "value2": priority,
            },
        )

        return data

    async def change_job_post_processing_options(self, nzo_id: str, options: int):
        data = await self._request(
            sabnzbd_method="change_opts",
            params={"value": nzo_id, "value2": options},
        )

        return data

    async def change_job_category(self, nzo_id: str, category: str):
        data = await self._request(
            sabnzbd_method="change_cat",
            params={"value": nzo_id, "value2": category},
        )

        return data

    async def set_speedlimit(self, limit: str | int | None):
        data = await self._request(
            sabnzbd_method="config", params={"name": "speedlimit", "value": limit}
        )
        return data["status"]

    async def history(
        self,
        start: int | None = None,
        limit: int | None = None,
        category: str | None = None,
        nzo_ids: list[str] | None = None,
    ):
        data = await self._request(
            sabnzbd_method="history",
            params={
                "start": start,
                "limit": limit,
                "category": category,
                "nzo_ids": nzo_ids,
            },
        )

        return data

    async def version(self):
        data = await self._request(sabnzbd_method="version")
        return data

    async def restart(self):
        data = await self._request(sabnzbd_method="restart")
        return data

    async def shutdown(self):
        data = await self._request(sabnzbd_method="shutdown")
        return data

    async def get_categories(self):
        data = await self._request(sabnzbd_method="get_cats")
        return data

    async def get_scripts(self):
        data = await self._request(sabnzbd_method="get_scripts")
        return data
