"""
Run pipes in different modes (iterative / multithreading)
"""
import os
from typing import Literal, TypeAlias, get_args
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from googleapiclient.errors import HttpError

from ...utils import handle_backup
from .pipe import IterablePipe, UniquePipe
from ...container import HttpErrorContainer


ignorableErrors: TypeAlias = Literal["commentsDisabled", "videoNotFound", "invalid"]
ignorableErrorsDescription = {
    "commentsDisabled": {
        "error_type": "forbidden (403)",
        "description": "The video identified by the videoId parameter has disabled comments."
    },
    "videoNotFound": {
        "error_type": "notFound (404)",
        "description": "The video identified by the videoId parameter couldn't be found."
    },
    "invalid": {
        "error_type": "invalidValue (400)",
        "description": "The API does not support the ability to list videos in the specified playlist. For example, you can't list a video in your watch later playlist."
    }
}

def safely_run_pipe(pipe: IterablePipe | UniquePipe, ignored_errors: list[HttpErrorContainer]) -> list[dict] | HttpErrorContainer | Exception:
    """
    Executes a data pipe safely, handling exceptions gracefully.
    """
    try:    
        items = pipe.run_pipe()
        return items
    except Exception as e:
        err = None
        if isinstance(e, (HttpError, )):
            err = HttpErrorContainer.from_http_error(e)
            # if the video's comment section is disabled, just proceed to next pipe execution
            if err.reason in get_args(ignorableErrors):
                ignored_errors.append(err)
                return []
        else:
            err = e
        return err


def run_pipe(
        pipe: IterablePipe | UniquePipe, 
        idx: int) -> tuple[int, list[dict] | HttpErrorContainer | Exception, list[HttpErrorContainer]]:
    ignored_errors: list[HttpErrorContainer] = list()
    result = safely_run_pipe(pipe, ignored_errors=ignored_errors)
    return (idx, result, ignored_errors)

def multithreading_run_pipe(
        pipes: list[IterablePipe | UniquePipe], ignored_errors: list[HttpErrorContainer],
        flatten_result=True, max_workers=8, backup_when_halted=False,
        output_folder="backup/IterableRetriever", filename=None
        ) -> list[dict] | list[list[dict]] | tuple[list[dict] | list[list[dict]], HttpErrorContainer | Exception]:
    """
    run pipes in multithreading form with a progress bar
    """
    raw_results: list[tuple[int, list[dict]]] = list()

    def sort_results_to_items(results: list[tuple[int, list[dict]]]) -> list[dict] | list[list[dict]]:
        raw_items = list()
        for r in sorted(results, key=lambda x: x[0]):
            _idx, _raw_items = r
            if flatten_result:
                # print(flatten_result)
                # print(len(_raw_items))
                raw_items.extend(_raw_items)
            else:
                raw_items.append(_raw_items)
        return raw_items
    
    error = None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(run_pipe, pipe, idx)
            for idx, pipe in enumerate(pipes)
        ]

        width = 3   # width of formatted text
        bar = tqdm(as_completed(futures), total=len(futures))
        
        for idx, future in enumerate(bar):
            _idx, item, _ignored_errors = future.result()
            bar.set_description("{:^{}s} / {:^{}s} batch(s) retrieved".format(str(idx+1), width, str(len(futures)), width))
            # normal results or ignorable error exists: proceed
            if isinstance(item, list):
                ignored_errors.extend(_ignored_errors)
                raw_results.append((_idx, item))

            # unignorable error exists: halt execution
            else:
                error = item
                print("ERR:", error)
                bar.set_description("Pipe halted due to error.")
                break
        bar.close()

    raw_items = sort_results_to_items(raw_results)

    if backup_when_halted:
        handle_backup(raw_items, output_folder=output_folder, filename=filename)

    if error is None:
        return raw_items
    else:
        return raw_items, error
    
    
def iterating_run_pipe(
        pipes: list[IterablePipe | UniquePipe], ignored_errors: list[HttpErrorContainer], flatten_result=True,
        output_folder="backup/IterableRetriever", filename=None, backup_when_halted=False
    ) -> list[dict] | list[list[dict]] | tuple[list[dict] | list[list[dict]], HttpErrorContainer | Exception]:
    """
    run pipes in iterative form with a progress bar
    """
    raw_items: list[dict] = []
    # page_infos: list[dict] = list()

    count = 0
    total = len(pipes)
    width = 3   # width of formatted text
    bar = tqdm(total=total)

    for pipe in pipes:
        result = safely_run_pipe(pipe, ignored_errors)
        # normal results or ignorable error exists: proceed
        if isinstance(result, list):
            items = result
        # unignorable error exists: halt execution
        else:
            error = result
            bar.set_description("Pipe halted due to error.")
            bar.close()
            if backup_when_halted:
                handle_backup(raw_items, output_folder=output_folder, filename=filename)
            return raw_items, error

        # page_infos.append(pipe._page_info)
        # filter empty items
        if items:
            if flatten_result:
                raw_items.extend(items)
            else:
                raw_items.append(items)
        
        bar.update()
        count += 1
        bar.set_description("{:^{}s} / {:^{}s} batch(s) retrieved".format(str(count), width, str(total), width))
            
    bar.close()

    return raw_items