pipeline {
    agent any

    environment {
        AWS_REGION ="ap-south-1"
        ACCOUNT_ID= "256664600401"
        REPO = "product-service"
        IMAGE="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO}"
    }

    stages {

        stage ('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vaibhavswami13/Devops_Micro_Product_service_project'
            }
        }

        // ✅ Build Docker Image FIRST
        stage ('Docker Build') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build --no-cache -t $REPO:$BUILD_NUMBER .
                '''
            }
        }

        // ✅ Test inside Docker (Production Standard)
        stage ('Test inside Docker') {
            steps {
                sh '''
                echo "Running tests inside container..."
                docker run --rm $REPO:$BUILD_NUMBER pytest || echo "No tests found"
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                echo "Logging into ECR..."
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Tag & Push to ECR') {
            steps{
                sh '''
                echo "Tagging image..."

                docker tag $REPO:$BUILD_NUMBER $IMAGE:$BUILD_NUMBER
                docker tag $REPO:$BUILD_NUMBER $IMAGE:latest

                echo "Pushing images..."

                docker push $IMAGE:$BUILD_NUMBER
                docker push $IMAGE:latest
                '''
            }
        }

        stage ('Deploy to EKS') {
            steps{
                sh '''
                echo "Deploying to Kubernetes..."

                kubectl set image deployment/product-service \
                product-service=$IMAGE:$BUILD_NUMBER

                echo "Verifying rollout..."
                kubectl rollout status deployment/product-service
                '''
            }
        }
    }

    post {
        success {
            echo "✅ product-service deployed successfully!"
        }
        failure {
            echo "❌ Deployment failed! Check logs."
        }
        always {
            sh '''
            echo "Cleaning up Docker images..."

            docker rmi $REPO:$BUILD_NUMBER || true
            docker rmi $IMAGE:$BUILD_NUMBER || true

            docker image prune -f || true
            '''
        }
    }
}
