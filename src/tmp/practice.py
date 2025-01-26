import httpx
import asyncio


class CallAPI:

    def __init__(self):
        self.base_url = 'https://github.com/NewBarrel41/'

    async def _call(self, session, url, cid):
        response = await session.get(url)
        await asyncio.sleep(1)
        return response.reason_phrase + cid

    async def _main(self, ec):
        async with httpx.AsyncClient() as client:
            cor = [self._call(client, self.base_url+e, c) for e, c in ec]
            response = await asyncio.gather(*cor)
            return response

    def main(self):
        cids = ['1', '2', '3']
        urls = ['new_project_jk', 'new_project_jk', 'new_project_jk']
        response = asyncio.run(self._main(zip(urls, cids)))
        return response


# if __name__ == "__main__":
#     call_api = CallAPI()
#     result = call_api.main()
#     print(result)
