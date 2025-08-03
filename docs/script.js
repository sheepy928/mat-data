let claimCount = 1;
let stepCounts = {0: 1};

function updateCodeUrlRequirement() {
    const claimType = document.querySelector('input[name="claim_type"]:checked').value;
    const codeUrlInput = document.getElementById('code_url');
    const codeUrlRequired = document.getElementById('code_url_required');
    const codeUrlHint = document.getElementById('code_url_hint');
    
    if (claimType === 'pip_libraries') {
        codeUrlInput.removeAttribute('required');
        codeUrlRequired.style.display = 'none';
        codeUrlHint.textContent = 'GitHub or other repository URL (optional for pip-installable claims)';
    } else {
        codeUrlInput.setAttribute('required', 'required');
        codeUrlRequired.style.display = 'inline';
        codeUrlHint.textContent = 'GitHub or other repository URL';
    }
}

function addStep(claimIndex) {
    const container = document.getElementById(`instructions_${claimIndex}`);
    const stepIndex = stepCounts[claimIndex] || 0;
    
    const stepDiv = document.createElement('div');
    stepDiv.className = 'instruction-step';
    stepDiv.innerHTML = `
        <input type="text" name="instruction_${claimIndex}_${stepIndex}" placeholder="Step ${stepIndex + 1}" required>
        <button type="button" class="btn-remove-step" onclick="removeStep(${claimIndex}, ${stepIndex})">×</button>
    `;
    
    container.appendChild(stepDiv);
    stepCounts[claimIndex] = stepIndex + 1;
}

function removeStep(claimIndex, stepIndex) {
    const container = document.getElementById(`instructions_${claimIndex}`);
    const steps = container.getElementsByClassName('instruction-step');
    
    if (steps.length > 1) {
        // Find and remove the specific step
        for (let step of steps) {
            const input = step.querySelector('input');
            if (input && input.name === `instruction_${claimIndex}_${stepIndex}`) {
                step.remove();
                break;
            }
        }
    }
}

function addClaim() {
    const container = document.getElementById('claimsContainer');
    
    const claimDiv = document.createElement('div');
    claimDiv.className = 'claim-block';
    claimDiv.setAttribute('data-claim-index', claimCount);
    
    claimDiv.innerHTML = `
        <h3>Claim ${claimCount + 1}</h3>
        <div class="form-group">
            <label for="claim_${claimCount}">Claim Description *</label>
            <textarea id="claim_${claimCount}" name="claim_${claimCount}" rows="3" required></textarea>
            <small>The specific claim from the paper you're documenting</small>
        </div>
        
        <div class="form-group">
            <label>Reproduction Instructions *</label>
            <div class="instructions-container" id="instructions_${claimCount}">
                <div class="instruction-step">
                    <input type="text" name="instruction_${claimCount}_0" placeholder="Step 1" required>
                    <button type="button" class="btn-remove-step" onclick="removeStep(${claimCount}, 0)">×</button>
                </div>
            </div>
            <button type="button" class="btn-add-step" onclick="addStep(${claimCount})">+ Add Step</button>
        </div>
        
        <button type="button" class="btn-remove-claim" onclick="removeClaim(${claimCount})">Remove Claim</button>
    `;
    
    container.appendChild(claimDiv);
    stepCounts[claimCount] = 1;
    claimCount++;
    
    // Show remove buttons on all claims when there's more than one
    updateRemoveButtons();
}

function removeClaim(claimIndex) {
    const claim = document.querySelector(`[data-claim-index="${claimIndex}"]`);
    if (claim) {
        claim.remove();
        delete stepCounts[claimIndex];
        updateRemoveButtons();
    }
}

function updateRemoveButtons() {
    const claims = document.querySelectorAll('.claim-block');
    const removeButtons = document.querySelectorAll('.btn-remove-claim');
    
    removeButtons.forEach(button => {
        button.style.display = claims.length > 1 ? 'block' : 'none';
    });
}

function resetForm() {
    if (confirm('Are you sure you want to reset the form? All data will be lost.')) {
        document.getElementById('submissionForm').reset();
        
        // Reset claims to just one
        const container = document.getElementById('claimsContainer');
        container.innerHTML = `
            <div class="claim-block" data-claim-index="0">
                <h3>Claim 1</h3>
                <div class="form-group">
                    <label for="claim_0">Claim Description *</label>
                    <textarea id="claim_0" name="claim_0" rows="3" required></textarea>
                    <small>The specific claim from the paper you're documenting</small>
                </div>
                
                <div class="form-group">
                    <label>Reproduction Instructions *</label>
                    <div class="instructions-container" id="instructions_0">
                        <div class="instruction-step">
                            <input type="text" name="instruction_0_0" placeholder="Step 1" required>
                            <button type="button" class="btn-remove-step" onclick="removeStep(0, 0)">×</button>
                        </div>
                    </div>
                    <button type="button" class="btn-add-step" onclick="addStep(0)">+ Add Step</button>
                </div>
                
                <button type="button" class="btn-remove-claim" onclick="removeClaim(0)" style="display: none;">Remove Claim</button>
            </div>
        `;
        
        claimCount = 1;
        stepCounts = {0: 1};
        
        // Hide output
        document.getElementById('output').style.display = 'none';
    }
}

function collectFormData() {
    const formData = new FormData(document.getElementById('submissionForm'));
    
    const data = {
        username: formData.get('username'),
        paper_title: formData.get('paper_title'),
        paper_pdf: formData.get('paper_pdf'),
        identifier: formData.get('identifier'),
        claim_type: formData.get('claim_type')
    };
    
    // Add code_url - required for custom_code, optional for pip_libraries
    const codeUrl = formData.get('code_url');
    if (codeUrl || data.claim_type === 'custom_code') {
        data.code_url = codeUrl;
    }
    
    // Add optional fields if present
    if (formData.get('data_url')) {
        data.data_url = formData.get('data_url');
    }
    
    // Collect claims
    data.claims = [];
    const claimBlocks = document.querySelectorAll('.claim-block');
    
    claimBlocks.forEach(block => {
        const claimIndex = block.getAttribute('data-claim-index');
        const claimText = formData.get(`claim_${claimIndex}`);
        
        if (claimText) {
            const instructions = [];
            const instructionInputs = block.querySelectorAll(`[name^="instruction_${claimIndex}_"]`);
            
            instructionInputs.forEach(input => {
                if (input.value.trim()) {
                    instructions.push(input.value.trim());
                }
            });
            
            if (instructions.length > 0) {
                data.claims.push({
                    claim: claimText,
                    instruction: instructions
                });
            }
        }
    });
    
    return data;
}

function generateOutput(format) {
    const data = collectFormData();
    
    if (format === 'json') {
        return JSON.stringify(data, null, 2);
    } else {
        // Use js-yaml if available, otherwise fall back to simple formatting
        if (typeof jsyaml !== 'undefined') {
            return jsyaml.dump(data);
        } else {
            // Simple YAML formatting
            let yaml = '';
            
            // Basic fields
            yaml += `username: "${data.username}"\n`;
            yaml += `paper_title: "${data.paper_title}"\n`;
            yaml += `paper_pdf: "${data.paper_pdf}"\n`;
            yaml += `identifier: "${data.identifier}"\n`;
            
            if (data.code_url) {
                yaml += `code_url: "${data.code_url}"\n`;
            }
            if (data.data_url) {
                yaml += `data_url: "${data.data_url}"\n`;
            }
            
            // Claims
            yaml += '\nclaims:\n';
            data.claims.forEach(claim => {
                yaml += `  - claim: "${claim.claim}"\n`;
                yaml += '    instruction:\n';
                claim.instruction.forEach(step => {
                    yaml += `      - "${step}"\n`;
                });
                yaml += '\n';
            });
            
            return yaml;
        }
    }
}

function copyToClipboard() {
    const content = document.getElementById('outputContent').textContent;
    navigator.clipboard.writeText(content).then(() => {
        alert('Content copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}

function downloadFile() {
    const content = document.getElementById('outputContent').textContent;
    const format = document.querySelector('input[name="format"]:checked').value;
    
    // Get username from form
    const username = document.getElementById('username').value.trim();
    
    // Generate UTC timestamp in format: YYYYMMDD_HHMMSS
    const now = new Date();
    const timestamp = now.getUTCFullYear() +
        String(now.getUTCMonth() + 1).padStart(2, '0') +
        String(now.getUTCDate()).padStart(2, '0') + '_' +
        String(now.getUTCHours()).padStart(2, '0') +
        String(now.getUTCMinutes()).padStart(2, '0') +
        String(now.getUTCSeconds()).padStart(2, '0');
    
    const filename = `${timestamp}_${username}.${format}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Form submission handler
document.getElementById('submissionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const format = document.querySelector('input[name="format"]:checked').value;
    const output = generateOutput(format);
    
    document.getElementById('outputContent').textContent = output;
    document.getElementById('output').style.display = 'block';
    
    // Scroll to output
    document.getElementById('output').scrollIntoView({ behavior: 'smooth' });
});