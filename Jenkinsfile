pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('Build') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]){
            sh 'pip install --user flask'
            sh 'pip install --user pyrebase'
            sh 'pip install --user Flask-WTF'
            sh 'pip install --user email_validator'
            sh 'pip install --user --upgrade firebase-admin'
            sh 'pip install --user json-e'
            sh 'pip install --user requests --upgrade'
            
        }
      }
    }
     
    stage('Cloning Git') {
      steps {
       git 'https://github.com/mor0981/ParkFlask.git'
      }
    }
    
    
    stage('test') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]){
          try{
            sh 'pip install --user pyrebase'
            sh 'python test2.py'
          }
          catch(er)
          {
            emailext body: "${er}", subject: 'Jenkis', to: 'mor0981@gmail.com'
          }
        }
      }   
    }

    

    
 
    
  }
}