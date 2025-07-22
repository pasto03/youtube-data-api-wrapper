"""
a terminal client that receive prompts for pipeline json building
"""
import sys
from typing import TypeAlias, Literal
from yt_pipeline.retriever.base.settings import RetrieveMethod

available_block_map = {
    "videos": ["comments", "captions"],
    "channels": ["playlists"],
    "search": ["videos", "channels", "playlists"],
    "playlists": ["playlist_items"],
    "playlist_items": ["videos"]
}

blockKeys: TypeAlias = Literal["videos", "channels", "search", "playlists", "playlist_items", "comments", "captions"]

class TerminalPipelineApp:
    @staticmethod
    def _prompt_available_blocks(last_block: dict | None = None) -> blockKeys | None:
        """
        prompt user to select a block key by available blocks
        """
        if not last_block:
            available_blocks = list(available_block_map.keys())
        else:
            block_name = last_block["foreman"]["name"]
            available_blocks = available_block_map.get(block_name)

        if not available_blocks:
            return

        print("Current Available Blocks:")
        for idx, block in enumerate(available_blocks):
            print("{}: {}".format(idx, block))

        # 'q' to exit; 'enter' to continue
        select_idx = input("\nEnter the index of block to be selected ('q' to exit, 'enter' to continue): ")
        if select_idx == "q":
            sys.exit()
        if select_idx == "":
            return
        assert select_idx.isdigit(), "Enter digit only"
        assert int(select_idx) < len(available_blocks), "Entered number outside available choices"
        selected_block_key = available_blocks[int(select_idx)]
        return selected_block_key
    
    @staticmethod
    def _propmt_infinite_params(id_type: Literal["videoId", "channelId", "playlistId", "itemId"] = "itemId") -> list[str]:
        """
        infinitely receives string ids until user quit (equivalent to clicking "+" to add id)
        """
        initial_input = list()
        while True:
            input_id = input(f"Enter your {id_type} ('q' to exit): ")
            if input_id == "q":
                assert initial_input, "Invalid params input. At least one itemId should be inserted."
                return initial_input
            initial_input.append(input_id)
    
    @staticmethod
    def _prompt_search_params():
        print("Search params:")
        params = dict()
        params["q"] = input("q: ")
        params["channelId"] = input("channelId: ") or None
        params["videoCategoryId"] = input("videoCategoryId: ") or None
        params["videoDuration"] = input("videoDuration: ") or "any"
        params["order"] = input("order: ") or "relevance"
        params["publishedAfter"] = input("publishedAfter: ") or None
        return params
    
    def _prompt_first_block_and_initial_input(self):
        # 1. Create first block
        block = self._create_block()

        # 2. Select initial input
        first_block_key = block["foreman"]["name"]
        initial_input = [self._prompt_search_params()] if first_block_key == "search" else self._propmt_infinite_params()
        return block, initial_input

    @staticmethod
    def _prompt_retrieval_methods():
        """
        prompt user to select retrieval method
        """
        retrieval_method = ["head", "custom", "all"]
        print("Retrieval Methods:")
        for idx, block in enumerate(retrieval_method):
            print("{}: {}".format(idx, block))
        select_idx = input("\nEnter the index of block to be selected: ")
        assert select_idx.isdigit(), "Enter digit only"
        assert int(select_idx) < len(retrieval_method), "Entered number outside available choices"
        retrieval = retrieval_method[int(select_idx)]
        return retrieval

    @staticmethod
    def _prompt_foreman_details(block_key: blockKeys):
        foreman = {"name": block_key}

        if block_key == "search":
            search_types = dict()
            search_types["video"] = input("video?(Y/n) ").lower() == "y"
            search_types["channel"] = input("channel?(Y/n) ").lower() == "y"
            search_types["playlist"] = input("playlist?(Y/n) ").lower() == "y"

            foreman["types"] = search_types

        return foreman
    
    def _prompt_settings(self, block_key: blockKeys):
        print("inside _prompt_settings")
        settings = dict()
        if block_key in ["search", "playlists", "playlist_items", "comments"]:
            retrieval: RetrieveMethod = self._prompt_retrieval_methods()
            settings["retrieval"] = retrieval

            match retrieval:
                case "all":
                    max_page = input("Max page: ")
                    assert max_page.isdigit(), "Enter integer only"
                    max_page = int(max_page)
                    assert max_page > 0, "Enter positive integer only"
                    settings["max_page"] = max_page

                case "custom":
                    n = input("n: ")
                    assert n.isdigit(), "Enter integer only"
                    n = int(n)
                    assert n > 0, "Enter positive integer only"
                    settings["n"] = n

        return settings
    
    def _create_block(self, last_block: dict = None):
        block = dict()

        # Step 2.1: Prompt for available block keys
        selected_block_key = self._prompt_available_blocks(last_block)

        if not selected_block_key:
            return

        # Step 2.2: Prompt for block details if applicable
        foreman = self._prompt_foreman_details(selected_block_key)
        block["foreman"] = foreman

        # Step 2.3: Prompt for settings
        settings = self._prompt_settings(selected_block_key)
        # print("built settings:", settings)
        block.update({"settings": settings} if settings else {})

        # Step 2.4: Prompt save output
        save_output = input("Save output? (Y/n)").lower() == "y"
        block['save_output'] = save_output

        # print("block in _create_block():", block)

        return block

    def invoke(self):
        stacks = dict()
        blocks = []

        # Step 1: Prompt for first block and relevant initial input
        block, initial_input = self._prompt_first_block_and_initial_input()
        stacks["initial_input"] = initial_input

        blocks.append(block)

        # Step 2: Loop for available blocks and prompts until no available blocks
        while block:
            # Step 2.1: create block
            block = self._create_block(blocks[-1])
            # print("New Block:", block)

            # Step 2.2: append block to blocks
            if block is not None:
                blocks.append(block)

        stacks["blocks"] = blocks

        # Step 3: Prompt for backup
        stacks["backup"] = input("Backup? (Y/n)").lower() == "y"

        return {"stacks": stacks}

    
# if __name__ == "__main__":
#     app = TerminalPipelineApp()
#     stacks = app.invoke()
#     print("Final stacks:", stacks)