%undefine _debugsource_packages

Name:		docker-cli
Version:	29.6.0
Release:	1
Source0:	https://github.com/docker/cli/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Summary:	Command line interface to the Docker container engine
URL:		https://github.com/docker-cli/docker-cli
License:	Apache-2.0
Group:		Servers
Recommends:	docker = %{version}
BuildRequires:	golang
BuildRequires:	go-md2man
BuildRequires:	make
Recommends:	(docker-zsh-completion = %{EVRD} if zsh)
Recommends:	(docker-fish-completion = %{EVRD} if fish)

%description
Command line interface to the Docker container engine

%package -n docker-fish-completion
Summary:        fish completion files for Docker
Requires:       %{name} = %{EVRD}
Requires:	fish

%description -n docker-fish-completion
Command line completion for Docker for the fish shell

%package -n docker-zsh-completion
Summary:        zsh completion files for Docker
Requires:       %{name} = %{EVRD}
Requires:       zsh

%description -n docker-zsh-completion
Command line completion for Docker for the zsh shell

%prep
%autosetup -p1 -n cli-%{version}

%build
mkdir -p src/github.com/docker
ln -s $(pwd) src/github.com/docker/cli
GOPATH=$(pwd) make VERSION=%{version} DOCKER_GITCOMMIT="OpenMandriva-%{version}-%{release}" DOCKER_CLI_EXPERIMENTAL=enabled LDFLAGS="-linkmode=external" DISABLE_WARN_OUTSIDE_CONTAINER=1 dynbinary manpages

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_mandir}
cp build/docker-%{_target_os}-* %{buildroot}%{_bindir}/docker
cp -a man/man? %{buildroot}%{_mandir}/

# install bash completion
install -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_sysconfdir}/bash_completion.d/docker.bash

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install fish completion
# create, install and own /usr/share/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/docker.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

%files
%{_bindir}/docker
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_sysconfdir}/bash_completion.d/docker.bash

%files -n docker-fish-completion
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/docker.fish

%files -n docker-zsh-completion
%{_datadir}/zsh/site-functions/_docker
