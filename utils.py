from urllib.parse import urlparse


def parse_timemap(timemap: str) -> dict:
    """
    Parse the timemap to a dictionary.
    :param timemap: Timemap to parse
    :return: Dictionary containing timemap values
    """

    timemap_dict = {"mementos": []}

    if timemap == "":
        return timemap_dict

    entries = timemap.split(",\n")
    for entry in entries:
        parts = entry.split("; ")

        uri = parts[0].replace("<", "").replace(">", "")
        rel = [part for part in parts if "rel=" in part]
        datetime = [part for part in parts if "datetime=" in part]
        if datetime:
            datetime = datetime[0].split("=")[1].replace('"', "")
        if rel:
            rel = rel[0].split("=")[1].replace('"', "")
            if rel == "original":
                timemap_dict["original"] = uri
            elif rel == "timegate":
                timemap_dict["timegate"] = uri
            elif datetime:
                if "memento" in rel:
                    timemap_dict["mementos"].append({"uri": uri, "datetime": datetime})
                if "first" in rel:
                    timemap_dict["first"] = uri
                if "last" in rel:
                    timemap_dict["last"] = uri
    return timemap_dict


def get_domain(link: str) -> str:
    """
    Get the domain from a link.
    :param link: Link to get domain from
    :return: Domain
    """
    parsed_link = urlparse(link)
    netloc = parsed_link.netloc
    splits = netloc.split(".")
    if len(splits) > 2:
        return ".".join(splits[-2:])
    return netloc
