i have copied mnist_model_best.pt from project_handwritten_digits, it has been created there

After creating the handler.py, 
create this directory but dont go into it:
mkdir -p model-store

after that run this command:
# Create model archive (.mar file)
torch-model-archiver \
  --model-name mnist-digit-classifier \
  --version 1.0 \
  --model-file handler.py \
  --serialized-file mnist_model_best.pt \
  --handler handler.py \
  --export-path model-store \
  --force

# This creates: model-store/mnist-digit-classifier.mar


Project 7 is copied from Project5 and added security scans

Run security scan semgrep (Add static code analysis)
semgrep --config=auto . --verbose

Run trivy scan (Implement container image vulnerability scanning)
trivy image mnist-torchserve:v1

Run gitleaks (Implement secret detection in pipeline)
git init 2>/dev/null || true                        - initialize git
git add .                                           - stage the files
git commit -m "Security scan" 2>/dev/null || true   - commit
gitleaks detect --no-git                            - run the secrets scan


Explore CBOM  & Secret Management ServServerServersServers ()Servers (Vault by HasHashiCorp)Explore SBOM & CBOM((CycloneDX) & Secret Management Servers (Vault by HashiCorp) 
syft mnist-torchserve:v1 -o cyclonedx-json > sbom.json

echo "Total components:"
cat sbom.json | jq '.components | length'
echo -e "\nTop 10 components:"
cat sbom.json | jq -r '.components[] | "\(.name) \(.version)"' | head -10



Run safety:
python3 -m safety check 


Run Vault:
# Start Vault in dev mode (for learning)
vault server -dev
# Leave that terminal running, open a NEW terminal and set environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='<USE THE TOKEN FROM FIRST TERMINAL>'
# Verify connection
vault status


Run the app like this:
python3 web_draw_test.py
kubectl port-forward -n kubeflow svc/mnist-torchserve 8080:8080