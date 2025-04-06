document.querySelectorAll('.requirement-header').forEach(header => {
    header.addEventListener('click', () => {
        const content = header.nextElementSibling;
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
    });
});

const chartBtn = document.getElementById('chartBtn');
const chartModal = document.getElementById('chartModal');
const closeChartModal = document.getElementById('closeChartModal');

chartBtn.addEventListener('click', function() {
    chartModal.style.display = 'block';
    createPieChart();
});

closeChartModal.addEventListener('click', function() {
    chartModal.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === chartModal) {
        chartModal.style.display = 'none';
    }
});

function createPieChart() {
    const pieChartContainer = document.getElementById('pieChartContainer');
    pieChartContainer.innerHTML = ''; 
    
    const completedCredits = 90; 
    const totalRequiredCredits = 120; 
    const remainingCredits = totalRequiredCredits - completedCredits;
    
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '300');
    svg.setAttribute('height', '300');
    svg.setAttribute('viewBox', '0 0 100 100');
    
    const completedPercentage = (completedCredits / totalRequiredCredits) * 100;
    const remainingPercentage = 100 - completedPercentage;
    
    const completedAngle = (completedPercentage / 100) * 360;
    const startAngle = 0;
    const endAngle = completedAngle;
    
    function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
        const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
        return {
            x: centerX + (radius * Math.cos(angleInRadians)),
            y: centerY + (radius * Math.sin(angleInRadians))
        };
    }
    
    function describeArc(x, y, radius, startAngle, endAngle) {
        const start = polarToCartesian(x, y, radius, endAngle);
        const end = polarToCartesian(x, y, radius, startAngle);
        const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1;
        return [
            "M", start.x, start.y,
            "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y,
            "L", x, y,
            "Z"
        ].join(" ");
    }
    
    const completedSegment = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    completedSegment.setAttribute('d', describeArc(50, 50, 40, 0, completedAngle));
    completedSegment.setAttribute('fill', '#0033A0'); 
    
    const remainingSegment = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    remainingSegment.setAttribute('d', describeArc(50, 50, 40, completedAngle, 360));
    remainingSegment.setAttribute('fill', '#F2C75C'); 
    
    svg.appendChild(completedSegment);
    svg.appendChild(remainingSegment);
    
    const legend = document.createElement('div');
    legend.style.display = 'flex';
    legend.style.flexDirection = 'column';
    legend.style.marginLeft = '20px';
    
    const completedLegend = document.createElement('div');
    completedLegend.style.display = 'flex';
    completedLegend.style.alignItems = 'center';
    completedLegend.style.marginBottom = '10px';
    
    const completedColor = document.createElement('div');
    completedColor.style.width = '20px';
    completedColor.style.height = '20px';
    completedColor.style.backgroundColor = '#0033A0';
    completedColor.style.marginRight = '10px';
    
    const completedText = document.createElement('span');
    completedText.textContent = `Completed: ${completedCredits} credits (${completedPercentage.toFixed(1)}%)`;
    completedText.style.color = '#1B2A47'; 
    completedText.style.fontWeight = '600';
    
    completedLegend.appendChild(completedColor);
    completedLegend.appendChild(completedText);
    
    const remainingLegend = document.createElement('div');
    remainingLegend.style.display = 'flex';
    remainingLegend.style.alignItems = 'center';
    
    const remainingColor = document.createElement('div');
    remainingColor.style.width = '20px';
    remainingColor.style.height = '20px';
    remainingColor.style.backgroundColor = '#F2C75C';
    remainingColor.style.marginRight = '10px';
    
    const remainingText = document.createElement('span');
    remainingText.textContent = `Remaining: ${remainingCredits} credits (${remainingPercentage.toFixed(1)}%)`;
    remainingText.style.color = '#1B2A47'; 
    remainingText.style.fontWeight = '600';
    
    remainingLegend.appendChild(remainingColor);
    remainingLegend.appendChild(remainingText);
    
    legend.appendChild(completedLegend);
    legend.appendChild(remainingLegend);
    
    const chartContainer = document.createElement('div');
    chartContainer.style.display = 'flex';
    chartContainer.style.alignItems = 'center';
    chartContainer.style.justifyContent = 'center';
    
    chartContainer.appendChild(svg);
    chartContainer.appendChild(legend);
    
    pieChartContainer.appendChild(chartContainer);
}