通過系計中運算資源貢獻此專案
===

### SSH connect with **port-forwarding**
```
ssh -L 8080:localhost:8080 110550071@172.30.17.213
```

連上後在瀏覽器打 localhost:8080 即可使用vscode

### Activate environment and update project
在vscode開啟terminal，並輸入下列幾行
```bash
conda activate ai
cd ~/AI-Final-Project
git fetch origin
git pull # If there's any difference, you need to update.
```

### Git push if you finish your job

```bash!
cd ~/AI-Final-Project
git fetch origin
git pull # If there's any difference, you need to update.
git add .
git status
git commit -m 'The-commit-message' # The commit message is a comment describing this push.
git push main # Or git push (If it fails)
```

### Exit the environment
```bash
conda deactivate
```

### Useful reference
[**如何用 Git & Github 與他人協作開發**](https://www.youtube.com/watch?v=AFMoQqH6t3A)