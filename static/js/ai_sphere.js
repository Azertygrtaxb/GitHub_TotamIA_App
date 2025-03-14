class AISphere {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.radius = 40;
        this.pulseRadius = 0;
        this.maxPulseRadius = 60;
        this.isPulsing = false;
        this.thinking = false;
        this.angle = 0;

        // Colors
        this.sphereColor = '#40E0D0';
        this.pulseColor = '#3A2618';
        
        this.animate();
    }

    drawSphere() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw pulse effect
        if (this.isPulsing) {
            this.ctx.beginPath();
            this.ctx.arc(this.canvas.width/2, this.canvas.height/2, this.pulseRadius, 0, Math.PI * 2);
            this.ctx.strokeStyle = this.pulseColor;
            this.ctx.lineWidth = 2;
            this.ctx.stroke();
            
            this.pulseRadius += 1;
            if (this.pulseRadius > this.maxPulseRadius) {
                this.pulseRadius = 0;
            }
        }

        // Draw main sphere
        this.ctx.beginPath();
        this.ctx.arc(this.canvas.width/2, this.canvas.height/2, this.radius, 0, Math.PI * 2);
        
        // Create gradient
        let gradient = this.ctx.createRadialGradient(
            this.canvas.width/2, this.canvas.height/2, 0,
            this.canvas.width/2, this.canvas.height/2, this.radius
        );
        gradient.addColorStop(0, '#7FFFD4');
        gradient.addColorStop(1, this.sphereColor);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fill();

        // Add dynamic effect when thinking
        if (this.thinking) {
            this.angle += 0.1;
            for (let i = 0; i < 3; i++) {
                let x = this.canvas.width/2 + Math.cos(this.angle + (i * Math.PI * 2/3)) * (this.radius + 10);
                let y = this.canvas.height/2 + Math.sin(this.angle + (i * Math.PI * 2/3)) * (this.radius + 10);
                
                this.ctx.beginPath();
                this.ctx.arc(x, y, 3, 0, Math.PI * 2);
                this.ctx.fillStyle = this.sphereColor;
                this.ctx.fill();
            }
        }
    }

    startThinking() {
        this.thinking = true;
        this.isPulsing = true;
    }

    stopThinking() {
        this.thinking = false;
        this.isPulsing = false;
    }

    pulse() {
        this.isPulsing = true;
        setTimeout(() => {
            this.isPulsing = false;
        }, 2000);
    }

    animate() {
        this.drawSphere();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize the AI sphere when the page loads
window.addEventListener('load', () => {
    window.aiSphere = new AISphere('aiSphere');
});
