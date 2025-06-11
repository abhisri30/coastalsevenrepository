from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def goto(self, path: str) -> None:
        await self.page.goto(path)
