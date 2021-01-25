
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

    githubPushRepo = "Cray-HPE/cfs-hwsync-agent"
    /*
        By default all branches are pushed to GitHub

        Optionally, to limit which branches are pushed, add a githubPushBranches regex variable
        Examples:
        githubPushBranches =  /master/ # Only push the master branch
        
        In this case, we push bugfix, feature, hot fix, master, and release branches

        NOTE: If this Jenkinsfile is removed, the a Jenkinsfile.github file must be created
        to do this push. See the cray-product-install-charts repo for an example.
    */
    githubPushBranches =  /(bugfix\/.*|feature\/.*|hotfix\/.*|master|release\/.*)/ 
}
