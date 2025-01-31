from datetime import datetime
from zoneinfo import ZoneInfo
from utils.utility import get_location_id


class TransformerService:
    @staticmethod
    def transform_response_access_to_spl_access(input_dict: dict) -> dict:
        """
        Transforms a dictionary of source access response to spl-access format .
        :param input_dict: Dictionary of source access response
        :return: Transformed dictionary of access
        """

        date = (
            input_dict.get("FECHA")
            if input_dict.get("FECHA")
            else datetime.now().strftime("%Y-%m-%d")
        )

        in_date = datetime.strptime(
            f"{date} {input_dict.get('TURNOINI')}", "%Y-%m-%d %H:%M:%S"
        )
        out_date = (
            None
            if not input_dict.get("TURNOFIN")
            else datetime.strptime(
                f"{date} {input_dict.get('TURNOFIN')}", "%Y-%m-%d %H:%M:%S"
            )
        )

        chile_tz = ZoneInfo("America/Santiago")

        transformed_dict = {
            "externalId": input_dict.get("IDCONTACTO", ""),
            "run": input_dict.get("RUT"),
            "fullName": input_dict.get("SOCIO", None),
            "location": f"{get_location_id(input_dict.get('SEDE')).value}",
            "entryAt": in_date.replace(tzinfo=chile_tz)
            .astimezone(ZoneInfo("UTC"))
            .strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        transformed_dict["exitAt"] = (
            out_date.replace(tzinfo=chile_tz)
            .astimezone(ZoneInfo("UTC"))
            .strftime("%Y-%m-%dT%H:%M:%SZ")
            if out_date
            else None
        )

        return transformed_dict
