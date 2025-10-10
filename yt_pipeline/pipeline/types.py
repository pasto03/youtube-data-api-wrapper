import json
import logging
from typing import Literal
from dataclasses import dataclass, field, asdict


@dataclass
class PipelineForemanDetails:
    name: str
    cost_per_call: int
        

@dataclass
class PipelineEstimationStage:
    foreman: PipelineForemanDetails = None
    n_input: int = None
    n_output: int = None
    item_multiplier: int = None
    max_page: int = None
    quota_usage: int = None
    staged_quota_cost: int = None


EstimationReportMetrics = Literal["items", "quota", "all"]


@dataclass
class PipelineEstimationReport:
    overall_cost: int = 0
    stages: list[PipelineEstimationStage] = field(default_factory=list)
    
    def to_json(self, output_path: str = None) -> None | dict:
        """
        convert object to json (and save to file if output_path specified)
        """
        output = asdict(self)
        if output_path:

            with open(output_path, "wb") as f:
                f.write(json.dumps(output, indent=4, ensure_ascii=False).encode("utf-8"))
        
            logging.info("file saved to {}".format(output_path))
        
        else:
            return output

    
    def display(self, metrics: EstimationReportMetrics = "quota"):
        """
        visualize report

        Format:
        - metrics = "items": [foreman_name] ({n_input} -> {n_output})
            - eg. `videos (2500 -> 2300)`
        - metrics = "quota": [foreman_name] ({quota_usage})
            - eg. `playlists (160)`
        - metrics = "all": [foreman_name] ({n_input} -> {n_output} | {quota_usage})
            - eg. `search (1 -> 50 | 200)`
        """
        print("Overall cost:", self.overall_cost)
        print("Structure:")
        for stage in self.stages:
            match metrics:
                case "items":
                    metric = f"{stage.n_input} -> {stage.n_output}"
                case "quota":
                    metric = f"{stage.quota_usage}"
                case "all":
                    metric = f"{stage.n_input} -> {stage.n_output} | {stage.quota_usage}"
                case _:
                    raise ValueError(f"invalid metrics type passed. ({EstimationReportMetrics})")
            print(f"{stage.foreman.name} ({metric})")