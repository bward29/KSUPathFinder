document.addEventListener('DOMContentLoaded', function () {
    let events = {
        "2025-02-27": [{
            title: "Players Guild Theatre: Willy Wonka",
            time: "7:30-10p",
            location: "Fine Arts Building - The Mary J. Timken Theatre",
            color: "#9370DB"
        }],
        "2025-03-05": [{
            title: "Ash Wednesday",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-03-09": [{
            title: "Daylight Saving Time",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-03-14": [{
            title: "Holi",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-03-17": [{
            title: "St. Patrick's Day",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-03-20": [{
            title: "Alumni and Current Faculty Concert",
            time: "7-8:30p",
            location: "Fine Arts Building - Music Addition - Room 114",
            color: "#4682B4"
        }],
        "2025-03-30": [{
            title: "Eid al-Fitr",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-03-31": [{
            title: "Eid al-Fitr (observed)",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-04-01": [{
            title: "April Fools' Day",
            time: "All Day",
            location: "",
            color: "#9370DB"
        }],
        "2025-04-02": [{
            title: "Voice Showcase",
            time: "7-8:30p",
            location: "Fine Arts Building - Music Addition - Room 114",
            color: "#4682B4"
        }]
    };

    const savedEvents = localStorage.getItem('calendarEvents');
    if (savedEvents) {
        try {
            const parsedEvents = JSON.parse(savedEvents);
            events = { ...events, ...parsedEvents };
        } catch (e) {
            console.error('Error parsing saved events:', e);
        }
    }

    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();
    let selectedDate = formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate());

    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

    function renderCalendar() {
        const container = document.getElementById('calendar-container');
        container.innerHTML = '';

        const viewOptions = createViewOptions();
        container.appendChild(viewOptions);

        const headerControls = createHeaderControls();
        container.appendChild(headerControls);

        const calendarGrid = createCalendarGrid();
        container.appendChild(calendarGrid);

        const eventPanel = document.createElement('div');
        eventPanel.className = 'event-panel';
        eventPanel.id = 'event-panel';
        container.appendChild(eventPanel);

        showEventPanel(selectedDate);
    }

    function createViewOptions() {
        const viewOptions = document.createElement('div');
        viewOptions.className = 'view-options';

        const options = ['Day', 'Week', 'Month', 'Year'];
        options.forEach(option => {
            const btn = document.createElement('button');
            btn.textContent = option;
            btn.className = 'view-option' + (option === 'Month' ? ' active' : '');
            viewOptions.appendChild(btn);
        });

        return viewOptions;
    }

    function createHeaderControls() {
        const headerControls = document.createElement('div');
        headerControls.className = 'controls-container';

        const navControls = document.createElement('div');
        navControls.className = 'navigation-controls';

        const prevBtn = document.createElement('button');
        prevBtn.innerHTML = '&lt;';
        prevBtn.className = 'nav-btn';
        prevBtn.addEventListener('click', function () {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            renderCalendar();
        });

        const monthYearTitle = document.createElement('h2');
        monthYearTitle.textContent = `${monthNames[currentMonth]} ${currentYear}`;

        const nextBtn = document.createElement('button');
        nextBtn.innerHTML = '&gt;';
        nextBtn.className = 'nav-btn';
        nextBtn.addEventListener('click', function () {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            renderCalendar();
        });

        const todayBtn = document.createElement('button');
        todayBtn.textContent = 'Today';
        todayBtn.className = 'today-btn';
        todayBtn.addEventListener('click', function () {
            currentMonth = today.getMonth();
            currentYear = today.getFullYear();
            selectedDate = formatDateStr(today.getFullYear(), today.getMonth() + 1, today.getDate());
            renderCalendar();
        });

        navControls.appendChild(prevBtn);
        navControls.appendChild(monthYearTitle);
        navControls.appendChild(nextBtn);
        navControls.appendChild(todayBtn);

        headerControls.appendChild(navControls);

        return headerControls;
    }

    function createCalendarGrid() {
        const grid = document.createElement('div');
        grid.className = 'calendar-grid';

        daysOfWeek.forEach(day => {
            const header = document.createElement('div');
            header.className = 'calendar-day-header';
            header.textContent = day;
            grid.appendChild(header);
        });

        const firstDay = new Date(currentYear, currentMonth, 1).getDay();
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        const prevMonthLastDay = new Date(currentYear, currentMonth, 0).getDate();
        const prevMonth = currentMonth === 0 ? 11 : currentMonth - 1;
        const prevMonthYear = currentMonth === 0 ? currentYear - 1 : currentYear;

        const nextMonth = currentMonth === 11 ? 0 : currentMonth + 1;
        const nextMonthYear = currentMonth === 11 ? currentYear + 1 : currentYear;

        for (let i = 0; i < firstDay; i++) {
            const day = prevMonthLastDay - firstDay + i + 1;
            const dateStr = formatDateStr(prevMonthYear, prevMonth + 1, day);
            const cell = createDayCell(day, 'prev-month', dateStr);
            grid.appendChild(cell);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = formatDateStr(currentYear, currentMonth + 1, day);
            const isToday = isCurrentDay(currentYear, currentMonth, day);

            const cell = createDayCell(day, isToday ? 'today' : '', dateStr);
            grid.appendChild(cell);
        }

        const totalCells = 42;
        const remainingCells = totalCells - (firstDay + daysInMonth);

        for (let day = 1; day <= remainingCells; day++) {
            const dateStr = formatDateStr(nextMonthYear, nextMonth + 1, day);
            const cell = createDayCell(day, 'next-month', dateStr);
            grid.appendChild(cell);
        }

        return grid;
    }

    function createDayCell(day, className, dateStr) {
        const cell = document.createElement('div');
        cell.className = `calendar-day ${className}`;

        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;

        if (className === 'today') {
            const circle = document.createElement('div');
            circle.className = 'today-circle';
            dayNumber.appendChild(circle);
        }

        cell.appendChild(dayNumber);

        if (events[dateStr] && events[dateStr].length > 0) {
            const eventsContainer = document.createElement('div');
            eventsContainer.className = 'day-events';

            events[dateStr].forEach((event, index) => {
                if (index < 2) {
                    const eventEl = document.createElement('div');
                    eventEl.className = 'event-indicator';
                    eventEl.textContent = event.title;
                    eventEl.style.backgroundColor = event.color || '#9370DB';
                    eventsContainer.appendChild(eventEl);
                } else if (index === 2) {
                    const moreEl = document.createElement('div');
                    moreEl.className = 'more-events';
                    moreEl.textContent = `+ ${events[dateStr].length - 2} more`;
                    eventsContainer.appendChild(moreEl);
                }
            });

            cell.appendChild(eventsContainer);
        }

        cell.addEventListener('click', function () {
            document.querySelectorAll('.calendar-day.active').forEach(el => {
                el.classList.remove('active');
            });

            cell.classList.add('active');
            selectedDate = dateStr;
            showEventPanel(dateStr);
        });

        if (dateStr === selectedDate) {
            cell.classList.add('active');
        }

        return cell;
    }

    function showEventPanel(dateStr) {
        const panel = document.getElementById('event-panel');
        if (!panel) return;

        panel.innerHTML = '';

        const date = parseDate(dateStr);
        const dayOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][date.getDay()];

        const header = document.createElement('div');
        header.className = 'event-panel-header';

        const dateTitle = document.createElement('h3');
        dateTitle.textContent = `${dayOfWeek}, ${monthNames[date.getMonth()]} ${date.getDate()}`;

        const addButton = document.createElement('button');
        addButton.className = 'add-event-btn';
        addButton.textContent = '+ Add Event';
        addButton.addEventListener('click', () => showAddEventForm(dateStr));

        header.appendChild(dateTitle);
        header.appendChild(addButton);
        panel.appendChild(header);

        const eventsList = document.createElement('div');
        eventsList.className = 'events-list';

        if (events[dateStr] && events[dateStr].length > 0) {
            events[dateStr].forEach((event, index) => {
                const eventItem = document.createElement('div');
                eventItem.className = 'event-item';
                eventItem.style.borderLeftColor = event.color || '#9370DB';

                const timeEl = document.createElement('div');
                timeEl.className = 'event-time';
                timeEl.textContent = event.time;

                const titleEl = document.createElement('div');
                titleEl.className = 'event-title';
                titleEl.textContent = event.title;

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-event-btn';
                deleteBtn.innerHTML = '×';
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    deleteEvent(dateStr, index);
                });

                eventItem.appendChild(timeEl);
                eventItem.appendChild(titleEl);

                if (event.location) {
                    const locationEl = document.createElement('div');
                    locationEl.className = 'event-location';
                    locationEl.textContent = event.location;
                    eventItem.appendChild(locationEl);
                }

                eventItem.appendChild(deleteBtn);
                eventsList.appendChild(eventItem);
            });
        } else {
            const noEvents = document.createElement('div');
            noEvents.className = 'no-events';
            noEvents.textContent = 'No events scheduled for this day';
            eventsList.appendChild(noEvents);
        }

        panel.appendChild(eventsList);
    }

    function showAddEventForm(dateStr) {
        const panel = document.getElementById('event-panel');
        panel.innerHTML = '';

        const date = parseDate(dateStr);

        const formTitle = document.createElement('h3');
        formTitle.textContent = `Add Event - ${monthNames[date.getMonth()]} ${date.getDate()}`;
        panel.appendChild(formTitle);

        const form = document.createElement('form');
        form.className = 'add-event-form';

        const titleGroup = document.createElement('div');
        titleGroup.className = 'form-group';

        const titleLabel = document.createElement('label');
        titleLabel.htmlFor = 'event-title';
        titleLabel.textContent = 'Title:';

        const titleInput = document.createElement('input');
        titleInput.type = 'text';
        titleInput.id = 'event-title';
        titleInput.required = true;

        titleGroup.appendChild(titleLabel);
        titleGroup.appendChild(titleInput);
        form.appendChild(titleGroup);

        const timeGroup = document.createElement('div');
        timeGroup.className = 'form-group';

        const timeLabel = document.createElement('label');
        timeLabel.htmlFor = 'event-time';
        timeLabel.textContent = 'Time:';

        const timeInput = document.createElement('input');
        timeInput.type = 'text';
        timeInput.id = 'event-time';
        timeInput.placeholder = 'e.g. 7-8:30p or All Day';

        timeGroup.appendChild(timeLabel);
        timeGroup.appendChild(timeInput);
        form.appendChild(timeGroup);

        const locationGroup = document.createElement('div');
        locationGroup.className = 'form-group';

        const locationLabel = document.createElement('label');
        locationLabel.htmlFor = 'event-location';
        locationLabel.textContent = 'Location:';

        const locationInput = document.createElement('input');
        locationInput.type = 'text';
        locationInput.id = 'event-location';

        locationGroup.appendChild(locationLabel);
        locationGroup.appendChild(locationInput);
        form.appendChild(locationGroup);

        const colorGroup = document.createElement('div');
        colorGroup.className = 'form-group';

        const colorLabel = document.createElement('label');
        colorLabel.htmlFor = 'event-color';
        colorLabel.textContent = 'Color:';

        const colorSelect = document.createElement('select');
        colorSelect.id = 'event-color';

        const colors = [
            { name: 'Purple', value: '#9370DB' },
            { name: 'Blue', value: '#4682B4' },
            { name: 'Green', value: '#3CB371' },
            { name: 'Orange', value: '#FF8C00' },
            { name: 'Red', value: '#CD5C5C' }
        ];

        colors.forEach(color => {
            const option = document.createElement('option');
            option.value = color.value;
            option.textContent = color.name;
            colorSelect.appendChild(option);
        });

        colorGroup.appendChild(colorLabel);
        colorGroup.appendChild(colorSelect);
        form.appendChild(colorGroup);

        const buttons = document.createElement('div');
        buttons.className = 'form-buttons';

        const cancelBtn = document.createElement('button');
        cancelBtn.type = 'button';
        cancelBtn.className = 'cancel-btn';
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => showEventPanel(dateStr));

        const saveBtn = document.createElement('button');
        saveBtn.type = 'submit';
        saveBtn.className = 'save-btn';
        saveBtn.textContent = 'Save';

        buttons.appendChild(cancelBtn);
        buttons.appendChild(saveBtn);
        form.appendChild(buttons);

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const newEvent = {
                title: document.getElementById('event-title').value,
                time: document.getElementById('event-time').value || 'All Day',
                location: document.getElementById('event-location').value,
                color: document.getElementById('event-color').value
            };

            addEvent(dateStr, newEvent);
            showEventPanel(dateStr);
        });

        panel.appendChild(form);
        titleInput.focus();
    }

    function addEvent(dateStr, newEvent) {
        if (!events[dateStr]) {
            events[dateStr] = [];
        }

        events[dateStr].push(newEvent);
        saveEvents();
        renderCalendar();
    }

    function deleteEvent(dateStr, index) {
        if (events[dateStr] && events[dateStr][index]) {
            events[dateStr].splice(index, 1);

            if (events[dateStr].length === 0) {
                delete events[dateStr];
            }

            saveEvents();
            renderCalendar();
        }
    }

    function saveEvents() {
        localStorage.setItem('calendarEvents', JSON.stringify(events));
    }

    function formatDateStr(year, month, day) {
        return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    }

    function parseDate(dateStr) {
        const [year, month, day] = dateStr.split('-').map(Number);
        return new Date(year, month - 1, day);
    }

    function isCurrentDay(year, month, day) {
        const now = new Date();
        return day === now.getDate() &&
            month === now.getMonth() &&
            year === now.getFullYear();
    }

    renderCalendar();
});