# Monitor CI Pipeline - Actions Tab Guide

## How to Check GitHub Actions

### Step 1: Navigate to Actions Tab

1. Go to your repository:
   ```
   https://github.com/deewakar05/GitOps-driven-Microservices-Platform
   ```

2. Click on **"Actions"** tab (top menu)

3. You should see workflow runs listed

### Step 2: Find Your Workflow Run

Look for the most recent run with:
- **Workflow**: "CI Pipeline"
- **Commit**: "Test CI pipeline - trigger workflow"
- **Branch**: `main`
- **Status**: Yellow dot (running) or Green checkmark (success) or Red X (failed)

### Step 3: Click on the Workflow Run

Click on the workflow run to see detailed execution.

## What You'll See

### Workflow Run Overview

At the top, you'll see:
- **Status**: Running / Success / Failed
- **Duration**: How long it's been running
- **Commit**: The commit that triggered it
- **Branch**: main

### Jobs List

You'll see 5 jobs (or 4 if on a non-main branch):

1. **Test** (Parallel execution)
   - `user-service` tests
   - `order-service` tests
   - Status: ⏳ Running / ✅ Success / ❌ Failed

2. **Build** (Parallel execution)
   - `user-service` build
   - `order-service` build
   - Status: ⏳ Running / ✅ Success / ❌ Failed

3. **Push to ECR** (Only on main branch)
   - `user-service` push
   - `order-service` push
   - Status: ⏳ Running / ✅ Success / ❌ Failed

4. **Integration Test**
   - Full stack testing
   - Status: ⏳ Running / ✅ Success / ❌ Failed

5. **Security Summary**
   - Scan results compilation
   - Status: ⏳ Running / ✅ Success / ❌ Failed

## Job Status Indicators

### ✅ Green Checkmark
- Job completed successfully
- All steps passed

### ⏳ Yellow Circle
- Job is currently running
- Click to see live logs

### ❌ Red X
- Job failed
- Click to see error details

### ⚠️ Yellow Triangle
- Job completed with warnings
- Usually non-critical issues

## Click on a Job to See Details

### Job Details View

When you click on a job, you'll see:

1. **Job Summary**
   - Duration
   - Status
   - Steps executed

2. **Steps List**
   Each step shows:
   - Step name
   - Duration
   - Status (✅/❌/⏳)

3. **Logs**
   - Click on a step to see logs
   - Scroll to see detailed output

## What to Look For

### ✅ Success Indicators

**Test Job:**
```
======================== 11 passed in 0.41s ========================
======================== 13 passed in 0.44s ========================
```

**Build Job:**
```
Successfully built abc123def456...
Successfully tagged user-service:latest
```

**Push to ECR Job:**
```
✅ Successfully pushed <ecr-url>/user-service:<sha>
✅ Successfully pushed <ecr-url>/user-service:latest
```

**Integration Test:**
```
✅ Order creation successful
✅ Metrics endpoints working
```

### ❌ Failure Indicators

**Common Error Messages:**

1. **"Access Denied"**
   - AWS credentials issue
   - Check GitHub Secrets

2. **"Repository Not Found"**
   - ECR repository doesn't exist
   - Run Terraform to create it

3. **"Tests Failed"**
   - Check test logs for specific failures
   - Usually indicates code issues

4. **"Docker Build Failed"**
   - Check Dockerfile syntax
   - Verify build context

## Real-Time Monitoring

### While Job is Running

1. **Refresh the page** to see updates
2. **Click on running job** to see live logs
3. **Watch step-by-step execution**

### Expected Timeline

- **Test Job**: ~2-3 minutes
- **Build Job**: ~3-5 minutes
- **Push to ECR**: ~1-2 minutes
- **Integration Test**: ~2-3 minutes
- **Security Summary**: ~10 seconds

**Total**: ~8-13 minutes

## Troubleshooting

### If Job is Stuck

1. Check if it's actually running (logs updating)
2. Wait a few more minutes (some steps take time)
3. If stuck > 15 minutes, cancel and retry

### If Job Failed

1. **Click on the failed job**
2. **Click on the failed step**
3. **Scroll through logs** to find error
4. **Look for error messages** in red
5. **Check common issues** below

### Common Issues

#### Issue: "No valid credential sources found"
**Solution**: Check AWS credentials in GitHub Secrets

#### Issue: "Repository not found"
**Solution**: Verify ECR repository URLs in secrets

#### Issue: "Tests failed"
**Solution**: Check test logs for specific test failures

#### Issue: "Docker build failed"
**Solution**: Check Dockerfile and build context

## Quick Links

- **Actions Tab**: https://github.com/deewakar05/GitOps-driven-Microservices-Platform/actions
- **Latest Run**: https://github.com/deewakar05/GitOps-driven-Microservices-Platform/actions/workflows/ci.yml
- **Secrets**: https://github.com/deewakar05/GitOps-driven-Microservices-Platform/settings/secrets/actions

## What to Do After Pipeline Completes

### If Successful ✅

1. **Verify ECR Images**
   - Go to AWS Console → ECR
   - Check repositories have new images

2. **Check Security Scans**
   - Go to Security tab
   - Review Trivy scan results

3. **Review Test Results**
   - Download test artifacts if needed
   - Check coverage reports

4. **Celebrate!** 🎉
   - CI/CD pipeline is working!
   - Ready for Phase 3

### If Failed ❌

1. **Read error logs** carefully
2. **Check GitHub Secrets** are correct
3. **Verify ECR repositories** exist
4. **Fix the issue** and push again
5. **Re-run workflow** or push new commit

## Monitoring Checklist

- [ ] Opened Actions tab
- [ ] Found latest workflow run
- [ ] Clicked on workflow run
- [ ] Checked all 5 jobs status
- [ ] Reviewed job logs if any failed
- [ ] Verified ECR push (if on main branch)
- [ ] Checked security scan results
- [ ] All jobs passed ✅

---

**Current Status**: Check the Actions tab now to see your pipeline running! 🚀
