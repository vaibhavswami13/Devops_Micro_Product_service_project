pipeline {
    agent any
    environment {
        AWS_REGION ="ap-south-1"
        ACCOUNT_ID= "256664600401"
        REPO = "product-service"
        IMAGE="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO}"
        }
    stages {
        stage ('checkout') {
            steps {
                git branch:'main',url:"https://github.com/vaibhavswami13/Devops_Micro_Product_service_project"
            }
        }
        stage('build & test') {
            steps {
                sh'''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }
        stage ('docker build') {
            steps {
                sh'''
                docker build --no-cache -t $REPO:$BUILD_NUMBER .
                '''
            }
        }
        stage('ECR Login') {
            steps {
                sh'''
                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }
        stage('docker tag and push to ECR') {
            steps{
                sh'''
                docker tag $REPO:$BUILD_NUMBER $IMAGE:$BUILD_NUMBER
                docker tag $REPO:$BUILD_NUMBER $IMAGE:latest
                docker push $IMAGE:$BUILD_NUMBER
                docker push $IMAGE:latest
                '''
            }
        }
        stage ('deploy to eks') {
            steps{
                sh'''
                kubectl set image deployment/product-service product-service=$IMAGE:$BUILD_NUMBER
                kubectl rollout status deployment/product-service
                '''
            }
        }
        post{
            success{
                echo "product-service app running successfully "
            }
            failure{
                echo " failed deployment! check logs"
            }
            always {
                sh'''
                echo "cleaning up docker image..."
                docker rmi $REPO:$BUILD_NUMBER || TRUE
                docker rmi $IMAGE:$BUILD_NUMBER || TRUE
                docker image prune -f || TRUE
                '''
            }
        }
    }
}
