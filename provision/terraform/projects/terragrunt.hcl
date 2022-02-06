remote_state {
    backend = "s3"
    generate = {
        path      = "_backend.tf"
        if_exists = "overwrite"
    }
    config = {
        bucket         = "awsterraform-terraform-backend"
        profile        = "gatheluck-admin"
        region         = "ap-northeast-1"
        encrypt        = true
        key = "projects/${path_relative_to_include()}"
    }
}

terraform {
    extra_arguments "common" {
        commands = get_terraform_commands_that_need_vars()

        required_var_files = [
            abspath(find_in_parent_folders("common.tfvars")),
        ]
    }
}