
@Library('dst-shared@release/shasta-1.4') _

dockerBuildPipeline {
    repository = "cray"
    imagePrefix = ""
    app = "cfs-hwsync-agent"
    name = "cfs-hwsync-agent"
    description = "Configuration Framework Service Hardware Synchronization Agent"
    product = "csm"
    enableSonar = true
    receiveEvent = ["k8s-liveness:master"]
}
