#!/usr/bin/env bash
set -eu

export ARCH="${KUBE_ARCH:-`dpkg --print-architecture`}"
KUBE_ARCH=${ARCH}

export KUBE_ARCH
export ETCD_VERSION="${ETCD_VERSION:-v3.4.3}"
export CNI_VERSION="${CNI_VERSION:-v0.8.7}"

# RUNC commit matching the containerd release commit
# Tag 1.5.11
export CONTAINERD_COMMIT="${CONTAINERD_COMMIT:-3df54a852345ae127d1fa3092b95168e4a88e2f8}"
# Release v1.0.3
export RUNC_COMMIT="${RUNC_COMMIT:-f46b6ba2c9314cfc8caae24a32ec5fe9ef1059fe}"
# Set this to the kubernetes fork you want to build binaries from
export KUBERNETES_REPOSITORY="${KUBERNETES_REPOSITORY:-github.com/kubernetes/kubernetes}"