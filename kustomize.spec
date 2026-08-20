# Copyright 2026 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: kustomize
Epoch: 100
Version: 5.7.1
Release: 1%{?dist}
Summary: Customization of kubernetes YAML configurations
License: Apache-2.0
URL: https://github.com/kubernetes-sigs/kustomize/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.27
BuildRequires: glibc-static

%description
kustomize lets you customize raw, template-free YAML files for multiple
purposes, leaving the original YAML untouched and usable as is.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
pushd kustomize && \
    export CGO_ENABLED=1 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w" \
        -o ../bin/kustomize . && \
popd

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -d %{buildroot}%{_prefix}/share/bash-completion/completions
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/kustomize
./bin/kustomize completion bash > %{buildroot}%{_prefix}/share/bash-completion/completions/kustomize

%files
%license LICENSE
%{_bindir}/*
%{_prefix}/share/bash-completion/completions/*

%changelog
