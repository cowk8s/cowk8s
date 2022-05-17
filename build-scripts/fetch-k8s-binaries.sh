#!/bin/bash
set -eu

apps="kubectl kube-apiserver kube-controller-manager kube-scheduler kubelet kube-proxy"
mkdir -p $KUBE_SNAP_BINS
echo $KUBE_VERSION > $KUBE_SNAP_BINS/version