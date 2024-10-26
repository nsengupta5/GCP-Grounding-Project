import hcl2


def get_tfvars(file_path: str) -> dict:
    with open(file_path, "r") as tfvars_fp:
        tfvars = hcl2.load(tfvars_fp)
    return tfvars
