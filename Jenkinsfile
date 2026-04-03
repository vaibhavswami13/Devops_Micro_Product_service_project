pipeline {
    agent any
    environment{
        IMAGE_NAME="product-service"
    }
    stages{
        stage('checkout'){
            steps{
                git branch: 'main', url: "https://github.com/vaibhavswami13/aws-devops-microservice-project"
            }
        }
        stage ('Build Docker Image'){
            steps {
                sh'''
                echo "building docker image"
                docker build -t $IMAGE_NAME:latest .
                '''
            }
        }
        stage ('Run app code test Inside Container'){
            steps{
                sh'''
                echo "running test"
                docker run --rm $IMAGE_NAME:latest pytest --maxfail=1 --disable-warnings -v || true
                '''
            }
        }
        stage ('Deploy container'){
            steps {
                sh'''
                echo "remove old containers if available"
                docker stop $IMAGE_NAME || true
                docker rm $IMAGE_NAME || true
                
                echo "running new container"
                docker run -d --name $IMAGE_NAME -p 5000:5000 --restart=always $IMAGE_NAME:latest
                '''
            }
        }
    }
    post{
        success{
            echo "application deployed successfully! access using url:http://<ec2>:5000"
        }
        failure{
            echo "app deployment failed! check logs"
        }
    }
}
