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

    let currentCredits = 90; 
const totalCreditsRequired = 120;
const startingCredits = currentCredits;

const semesterCourses = {
    Spring2025: [
        { code: "CS 35201", credits: 3 },
        { code: "CS 33901", credits: 3 },
        { code: "CS 44001", credits: 3 },
        { code: "CS 46101", credits: 4 }
    ],
    Summer2025: [],
    Fall2025: [],
    Spring2026: []
};

const academicTab = document.querySelector('.tab:nth-child(1)');
const whatIfTab = document.querySelector('.tab:nth-child(2)');
const academicContent = document.getElementById('academic-content');
const whatIfContent = document.getElementById('what-if-content');

function updateTabDisplay() {
    if (academicTab.classList.contains('active')) {
        academicContent.style.display = 'block';
        whatIfContent.style.display = 'none';
    } else {
        academicContent.style.display = 'none';
        whatIfContent.style.display = 'block';
        updateWhatIfProgress();
    }
}

academicTab.addEventListener('click', function() {
    academicTab.classList.add('active');
    whatIfTab.classList.remove('active');
    updateTabDisplay();
});

whatIfTab.addEventListener('click', function() {
    whatIfTab.classList.add('active');
    academicTab.classList.remove('active');
    updateTabDisplay();
});

function updateWhatIfProgress() {
    let totalCredits = startingCredits;
    for (const semester in semesterCourses) {
        semesterCourses[semester].forEach(course => {
            totalCredits += course.credits;
        });
    }
    
    const whatIfCreditsElement = document.getElementById('what-if-credits');
    const whatIfPercentageElement = document.getElementById('what-if-percentage');
    const whatIfProgressBar = document.getElementById('what-if-progress-bar');
    const completionMessage = document.getElementById('completion-message');
    
    const percentage = Math.min(Math.round((totalCredits / totalCreditsRequired) * 100), 100);
    
    whatIfCreditsElement.textContent = `${totalCredits}/${totalCreditsRequired}`;
    whatIfPercentageElement.textContent = `${percentage}%`;
    whatIfProgressBar.style.width = `${percentage}%`;
    
    if (totalCredits >= totalCreditsRequired) {
        completionMessage.style.display = 'block';
    } else {
        completionMessage.style.display = 'none';
    }
}
const courseSelectionModal = document.getElementById('courseSelectionModal');
const closeCourseModal = document.getElementById('closeCourseModal');
const courseSearch = document.getElementById('courseSearch');
const courseOptions = document.querySelectorAll('.course-option');
const addSelectedCourseBtn = document.getElementById('addSelectedCourseBtn');
const manualCourseCode = document.getElementById('manualCourseCode');
const manualCourseCredits = document.getElementById('manualCourseCredits');

let currentSemester = '';

function updateAvailableCourses() {
    const selectedCourses = [];
    for (const semester in semesterCourses) {
        semesterCourses[semester].forEach(course => {
            selectedCourses.push(course.code);
        });
    }
    
    document.querySelectorAll('.course-option').forEach(option => {
        const courseCode = option.dataset.code;
        
        if (selectedCourses.includes(courseCode)) {
            option.classList.add('disabled');
            option.classList.remove('selected'); 
        } else {
            option.classList.remove('disabled');
        }
    });
}

document.querySelectorAll('.add-course-btn').forEach(button => {
    button.addEventListener('click', function() {
        currentSemester = this.dataset.semester;
        courseSelectionModal.style.display = 'block';
        resetCourseSelection();
        updateAvailableCourses(); 
    });
});

closeCourseModal.addEventListener('click', function() {
    courseSelectionModal.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === courseSelectionModal) {
        courseSelectionModal.style.display = 'none';
    }
});

function resetCourseSelection() {
    courseSearch.value = '';
    manualCourseCode.value = '';
    manualCourseCredits.value = '';
    courseOptions.forEach(option => {
        option.classList.remove('selected');
        option.style.display = 'flex';
    });
    document.querySelector('.no-results').style.display = 'none';
}

courseSearch.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    let resultsFound = false;
    
    courseOptions.forEach(option => {
        const code = option.dataset.code.toLowerCase();
        const name = option.querySelector('.course-option-name').textContent.toLowerCase();
        
        if (code.includes(searchTerm) || name.includes(searchTerm)) {
            option.style.display = 'flex';
            resultsFound = true;
        } else {
            option.style.display = 'none';
        }
    });
    
    document.querySelector('.no-results').style.display = resultsFound ? 'none' : 'block';
});

courseOptions.forEach(option => {
    option.addEventListener('click', function() {
        if (!this.classList.contains('disabled')) {
            courseOptions.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            
            manualCourseCode.value = '';
            manualCourseCredits.value = '';
        }
    });
});

addSelectedCourseBtn.addEventListener('click', function() {
    let courseCode, courseCredits;
    
    const selectedOption = document.querySelector('.course-option.selected');
    
    if (selectedOption) {
        courseCode = selectedOption.dataset.code;
        courseCredits = parseInt(selectedOption.dataset.credits);
    } 
    
    else if (manualCourseCode.value && manualCourseCredits.value) {
        courseCode = manualCourseCode.value.toUpperCase();
        courseCredits = parseInt(manualCourseCredits.value);
        
        let courseAlreadySelected = false;
        for (const semester in semesterCourses) {
            semesterCourses[semester].forEach(course => {
                if (course.code === courseCode) {
                    courseAlreadySelected = true;
                }
            });
        }
        
        if (courseAlreadySelected) {
            alert('This course is already selected in another semester.');
            return;
        }
    } 
    
    else {
        alert('Please select a course or enter course details manually.');
        return;
    }
    
    semesterCourses[currentSemester].push({
        code: courseCode,
        credits: courseCredits
    });
    
    updateCourseList(currentSemester);
    
    updateWhatIfProgress();
    
    courseSelectionModal.style.display = 'none';
});
function updateCourseList(semester) {
    const courseListElement = document.getElementById(`${semester}-courses`);
    courseListElement.innerHTML = '';
    
    semesterCourses[semester].forEach((course, index) => {
        const courseItem = document.createElement('div');
        courseItem.className = 'course-item';
        
        const courseCode = document.createElement('span');
        courseCode.className = 'course-code';
        courseCode.textContent = course.code;
        
        const courseCredits = document.createElement('span');
        courseCredits.className = 'course-credits';
        courseCredits.textContent = `(${course.credits})`;
        
        const removeButton = document.createElement('button');
        removeButton.className = 'remove-course-btn';
        removeButton.textContent = '×';
        removeButton.dataset.index = index;
        removeButton.dataset.semester = semester;
        
        courseItem.appendChild(courseCode);
        courseItem.appendChild(courseCredits);
        courseItem.appendChild(removeButton);
        
        courseListElement.appendChild(courseItem);
    });
    
    document.querySelectorAll('.remove-course-btn').forEach(button => {
        if (button.dataset.semester && button.dataset.index !== undefined) {
            button.addEventListener('click', function() {
                const semester = this.dataset.semester;
                const index = parseInt(this.dataset.index);
                
                semesterCourses[semester].splice(index, 1);
                
                updateCourseList(semester);
                updateWhatIfProgress();
                updateAvailableCourses();
            });
        }
    });
}

for (const semester in semesterCourses) {
    updateCourseList(semester);
}

document.getElementById('saveWhatIfBtn').addEventListener('click', function() {
    alert('Your What-If plan has been saved!');
});

updateWhatIfProgress();

}