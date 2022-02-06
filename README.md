https://github.com/yuyasugano/terraform-sagemaker-sample-1
https://y-ohgi.com/introduction-terraform/

## Terraform and Terragrunt

### Version

We use following versions.
- [**terraform 1.1.3**](https://github.com/hashicorp/terraform/releases)
- [**terragrunt 0.36.1**](https://terragrunt.gruntwork.io/)

We recomend to use following to control terraform version.
- [tfenv](https://github.com/tfutils/tfenv)
- [tgenv](https://github.com/cunymatthieu/tgenv)

Following is sample installation process to Ubuntu (tested on Ubuntu 20.04).

```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt-get install build-essential curl file git

# install linuxbrew to install tfenv (following is installation for zsh)
$ test -d ~/.linuxbrew && PATH="$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin:$PATH"
$ test -d /home/linuxbrew/.linuxbrew && PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:$PATH"
$ test -r ~/.zshrc && echo "export PATH='$(brew --prefix)/bin:$(brew --prefix)/sbin'":'"$PATH"' >>~/.zshrc

# install tfenv and tgenv
$ brew doctor
$ brew install tfenv
$ brew install tgenv

# check if installation is successed
$ tfenv
$ tgenv

# select terraform version
$ tfenv list-remote  # check available versions 
$ tfenv install 1.1.3
$ tfenv use 1.1.3
$ tfenv list  # check currently used version 

# select terragrunt version
$ tgenv list-remote  # check available versions 
$ tgenv install 0.36.1
$ tgenv use 0.36.1
$ tgenv list  # check currently used version 
```

