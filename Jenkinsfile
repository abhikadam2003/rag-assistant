pipeline {
    agent any

    stages {

        stage('Deploy To Kubernetes Using Helm') {
            steps {

                withKubeCredentials(kubectlCredentials: [[
                    caCertificate: '',
                    clusterName: 'EKS-abhi',
                    contextName: '',
                    credentialsId: 'k8s-token',
                    namespace: 'webapps',
                    serverUrl: 'https://EF29B5EEBF2B868D381410AE8C701791.sk1.us-east-1.eks.amazonaws.com'
                ]]) {

                    sh '''
                    kubectl create namespace webapps --dry-run=client -o yaml | kubectl apply -f -

                    helm upgrade --install assistant-app ./helm \
                    -n webapps
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {

                withKubeCredentials(kubectlCredentials: [[
                    caCertificate: '',
                    clusterName: 'EKS-abhi',
                    contextName: '',
                    credentialsId: 'k8s-token',
                    namespace: 'webapps',
                    serverUrl: 'https://EF29B5EEBF2B868D381410AE8C701791.sk1.us-east-1.eks.amazonaws.com'
                ]]) {

                    sh 'kubectl get pods -n webapps'
                    sh 'kubectl get svc -n webapps'

                }
            }
        }
    }
}
