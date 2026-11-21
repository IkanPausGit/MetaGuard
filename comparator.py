
def compare_metadata(original, modified):
    if original.get("Format") != modified.get("Format"):
        raise ValueError(
            "Cannot compare different file formats. "
            "Please select two files of the same format."
        )

    ignored_fields = {"File Name", "Format"}

    added = {}
    removed = {}
    changed = {}
    unchanged = {}

    all_keys = (set(original) | set(modified)) - ignored_fields

    for key in sorted(all_keys):
        if key not in original:
            added[key] = modified[key]

        elif key not in modified:
            removed[key] = original[key]

        elif original[key] != modified[key]:
            changed[key] = {
                "before": original[key],
                "after": modified[key]
            }

        else:
            unchanged[key] = original[key]

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged
    }
