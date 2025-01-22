let sparkInterval;


const glowBtns = document.querySelectorAll('.glow-btn');
glowBtns.forEach(glowBtn => {
    glowBtn.addEventListener('mouseenter', () => {
        sparkInterval = setInterval(() => {
            for (let i = 0; i < 5; i++) createSpark(glowBtn);
        }, 100);
    });

    glowBtn.addEventListener('mouseleave', () => clearInterval(sparkInterval));
});

function createSpark(glowBtn) {
    const spark = document.createElement('div');
    spark.className = 'spark';
    
    const rect = glowBtn.getBoundingClientRect();
    const x = Math.random() * rect.width;
    const y = Math.random() * rect.height;

    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 50 + 30;
    const tx = Math.cos(angle) * speed;
    const ty = Math.sin(angle) * speed;

    const size = Math.random() * 4 + 2;

    spark.style.cssText = `
        left: ${x}px;
        top: ${y}px;
        --tx: ${tx}px;
        --ty: ${ty}px;
        width: ${size}px;
        height: ${size}px;
    `;

    glowBtn.append(spark);
    setTimeout(() => spark.remove(), 600);
}