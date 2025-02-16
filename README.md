java==23.0.2
OS==windows 10
Maven==3.8.8


mvn clean package
java -jar target/rule-engine-1.0-SNAPSHOT-jar-with-dependencies.jar

uvicorn main:app --reload --host 0.0.0.0 --port 8000