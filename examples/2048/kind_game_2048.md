# **Kind (Kubernetes IN Docker) - Deploying 2048 Game**

## **1️⃣ Setup Kind Cluster**
### **🔹 Install Kind (If Not Installed)**
#### **On Linux/macOS:**
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```
#### **On Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://kind.sigs.k8s.io/dl/latest/kind-windows-amd64" -OutFile kind.exe
```
Move `kind.exe` to a directory in your system **PATH**.

---

## **2️⃣ Create a Kind Cluster**
```bash
kind create cluster --name my-cluster
```
✅ **Verify the cluster is running:**
```bash
kubectl cluster-info --context kind-my-cluster
kubectl get nodes
```

---

## **3️⃣ Deploy the 2048 Game**
Apply the **2048 Kubernetes deployment**:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml
```
✅ **Check if everything is deployed properly:**
```bash
kubectl get all -n game-2048
```
You should see:
- **Pods**
- **Deployments**
- **Services (including `service-2048`)**

---

## **4️⃣ Port-Forward the Service**
```bash
kubectl port-forward svc/service-2048 8080:80 -n game-2048
```
✅ **Now, open your browser and visit:**  
👉 **http://localhost:8080**  

---

## **5️⃣ Check if Port 8080 is in Use**
Before forwarding the port, ensure that port **8080** is not already in use:
```powershell
netstat -ano | findstr :8080
```
If another process is using it, terminate it:
```powershell
taskkill /PID <PID> /F
```
Replace `<PID>` with the actual Process ID from the `netstat` output.

---

## **6️⃣ Delete the Namespace (Cleanup)**
Once you're done, delete everything by removing the `game-2048` namespace:
```bash
kubectl delete namespace game-2048
```
✅ **Confirm deletion:**
```bash
kubectl get namespaces
```
The `game-2048` namespace should no longer exist.

---

### 🎯 **Final Summary**
1. **Created a Kind Cluster**
2. **Deployed the 2048 Game**
3. **Checked for Port Conflicts (`netstat -ano | findstr :8080`)**
4. **Forwarded the Port (8080)**
5. **Played the Game**
6. **Deleted the Namespace for Cleanup**

This is a complete workflow from **Kind cluster creation** to **cleaning up the deployment**. 🚀 Let me know if you need modifications!
