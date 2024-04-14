# Running playbook locally

To create and run the VM, run the following command:
```bash
export PROXMOX_API_SECRET=[your_api_key_here]
export PROXMOX_USER=[your_proxmox_user_here]
export VM_USER_PASSWORD=[user_password_here]
ansible-playbook --extra-vars "api_token_secret=$PROXMOX_API_SECRET vm_user_password=$VM_USER_PASSWORD" -u $PROXMOX_USER -k -i local app_vm.yaml
```
