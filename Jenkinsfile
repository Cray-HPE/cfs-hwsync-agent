
@Library('dst-shared@release/shasta-1.3') _

dockerBuildPipeline {
    repository = "cray"
    imagePrefix = ""
    app = "cfs-hwsync-agent"
    name = "cfs-hwsync-agent"
    description = "Configuration Framework Service Hardware Synchronization Agent"
    product = "shasta-premium,shasta-standard"
    enableSonar = true
    receiveEvent = ["k8s-liveness:master"]
}
