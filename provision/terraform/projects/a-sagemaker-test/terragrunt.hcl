include {
    path = find_in_parent_folders()
}

terraform {
    source = "../..//projects/${path_relative_to_include()}"
}
