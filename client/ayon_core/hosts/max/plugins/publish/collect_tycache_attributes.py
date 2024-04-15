import pyblish.api
import copy
from ayon_core.lib import BoolDef
from ayon_core.pipeline.publish import AYONPyblishPluginMixin
from pymxs import runtime as rt


class CollectTyFlowData(pyblish.api.InstancePlugin,
                        AYONPyblishPluginMixin):
    """Collect Channel Attributes for TyCache Export"""

    order = pyblish.api.CollectorOrder + 0.005
    label = "Collect tyCache attribute Data"
    hosts = ['max']
    families = ["tyflow"]

    def process(self, instance):
        context = instance.context
        container = rt.GetNodeByName(instance.data["instance_node"])
        tyc_product_names = [
                name for name
                in container.modifiers[0].AYONTyCacheData.tyc_exports
        ]
        attr_values = self.get_attr_values_from_data(instance.data)
        # TODO: need to do regex when the export particle has some names without regex.
        for tyc_product_name in tyc_product_names:
            self.log.debug(f"Creating instance for operator:{tyc_product_name}")
            tyc_instance = context.create_instance(tyc_product_name)
            tyc_instance[:] = instance[:]
            tyc_instance.data.update(copy.deepcopy(dict(instance.data)))
            tyc_instance.data["name"] = tyc_product_name
            tyc_instance.data["label"] = tyc_product_name
            tyc_instance.data["family"] = instance.data["tyc_exportMode"]
            tyc_instance.data["productName"] = tyc_product_name
            tyc_instance.data["productType"] = instance.data["tyc_exportMode"]
            tyc_instance.data["exportMode"] = (
                2 if instance.data["tyc_exportMode"] == "tycache" else 6
            )
            tyc_instance.data["families"] = [instance.data["tyc_exportMode"]]
            tyc_instance.data["publish_attributes"] = {"ValidateTyCacheFrameRange":{"active": True}}
            instance.append(tyc_instance)

    @classmethod
    def get_attribute_defs(cls):
        return [
            BoolDef("has_frame_range_validator",
                    label="Validate TyCache Frame Range",
                    default=True),
        ]