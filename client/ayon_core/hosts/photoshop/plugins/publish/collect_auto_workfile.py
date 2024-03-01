import os
import pyblish.api

from ayon_core.client import get_asset_name_identifier
from ayon_core.hosts.photoshop import api as photoshop
from ayon_core.pipeline.create import get_product_name


class CollectAutoWorkfile(pyblish.api.ContextPlugin):
    """Collect current script for publish."""

    order = pyblish.api.CollectorOrder + 0.2
    label = "Collect Workfile"
    hosts = ["photoshop"]

    targets = ["automated"]

    def process(self, context):
        product_type = "workfile"
        file_path = context.data["currentFile"]
        _, ext = os.path.splitext(file_path)
        staging_dir = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        workfile_representation = {
            "name": ext[1:],
            "ext": ext[1:],
            "files": base_name,
            "stagingDir": staging_dir,
        }

        for instance in context:
            if instance.data["productType"] == product_type:
                self.log.debug("Workfile instance found, won't create new")
                instance.data.update({
                    "label": base_name,
                    "name": base_name,
                    "representations": [],
                })

                # creating representation
                _, ext = os.path.splitext(file_path)
                instance.data["representations"].append(
                    workfile_representation)

                return

        stub = photoshop.stub()
        stored_items = stub.get_layers_metadata()
        for item in stored_items:
            if item.get("creator_identifier") == product_type:
                if not item.get("active"):
                    self.log.debug("Workfile instance disabled")
                    return

        project_name = context.data["projectName"]
        proj_settings = context.data["project_settings"]
        auto_creator = proj_settings.get(
            "photoshop", {}).get(
            "create", {}).get(
            "WorkfileCreator", {})

        if not auto_creator or not auto_creator["enabled"]:
            self.log.debug("Workfile creator disabled, won't create new")
            return

        # context.data["variant"] might come only from collect_batch_data
        variant = (context.data.get("variant") or
                   auto_creator["default_variant"])

        task_name = context.data["task"]
        host_name = context.data["hostName"]
        asset_doc = context.data["assetEntity"]

        folder_path = get_asset_name_identifier(asset_doc)
        product_name = get_product_name(
            project_name,
            asset_doc,
            task_name,
            host_name,
            product_type,
            variant,
            project_settings=proj_settings
        )

        # Create instance
        instance = context.create_instance(product_name)
        instance.data.update({
            "label": base_name,
            "name": base_name,
            "productName": product_name,
            "productType": product_type,
            "family": product_type,
            "families": [product_type],
            "representations": [],
            "folderPath": folder_path
        })

        # creating representation
        instance.data["representations"].append(workfile_representation)

        self.log.debug("auto workfile review created:{}".format(instance.data))
