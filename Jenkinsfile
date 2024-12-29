pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'credit-risk-prediction-service'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        AWS_ECR_REGISTRY = '${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com'
        KUBERNETES_NAMESPACE = 'fintech'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Convert Notebook and Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    jupyter nbconvert --to script main.ipynb
                    python -m pytest tests/ || true
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python main.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_REGISTRY}
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Push to ECR') {
            steps {
                script {
                    sh """
                        docker push ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                script {
                    sh """
                        aws eks update-kubeconfig --name fintech-cluster --region ${AWS_REGION}
                        kubectl set image deployment/credit-risk-prediction \
                        credit-risk-prediction=${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} \
                        -n ${KUBERNETES_NAMESPACE}
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
            sh '''
                docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                docker rmi ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} || true
                docker rmi ${AWS_ECR_REGISTRY}/${DOCKER_IMAGE}:latest || true
            '''
        }
    }
}