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
                    namespace: 'rag',
                    serverUrl: 'https://EF29B5EEBF2B868D381410AE8C701791.sk1.us-east-1.eks.amazonaws.com'
                ]]) {

                    sh '''
                    helm upgrade --install frontend-app ./chart \
                    -n rag
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
                    namespace: 'rag',
                    serverUrl: 'https://EF29B5EEBF2B868D381410AE8C701791.sk1.us-east-1.eks.amazonaws.com'
                ]]) {

                    sh 'kubectl get pods -n rag'
                    sh 'kubectl get svc -n rag'

                }
            }
        }
    }
}
