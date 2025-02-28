const NORTH_CANTON = { lat: 40.8759, lon: -81.4029 };

async function getWeatherData() {
    try {
        const [currentResponse, forecastResponse] = await Promise.all([
            fetch(`${CONFIG.BASE_URL}/weather?lat=${NORTH_CANTON.lat}&lon=${NORTH_CANTON.lon}&appid=${CONFIG.API_KEY}&units=${CONFIG.UNITS}`),
            fetch(`${CONFIG.BASE_URL}/forecast?lat=${NORTH_CANTON.lat}&lon=${NORTH_CANTON.lon}&appid=${CONFIG.API_KEY}&units=${CONFIG.UNITS}`)
        ]);

        const [currentData, forecastData] = await Promise.all([
            currentResponse.json(),
            forecastResponse.json()
        ]);

        displayWeather(currentData, forecastData);
    } catch (error) {
        console.error('Weather error:', error);
    }
}

function displayWeather(current, forecast) {
    const weatherBox = document.getElementById('weather-display');
    const temp = Math.round(current.main.temp);

    // Process forecast data
    const dailyForecasts = {};
    forecast.list.forEach(item => {
        const date = new Date(item.dt * 1000);
        const dateKey = date.toLocaleDateString();

        if (!dailyForecasts[dateKey]) {
            dailyForecasts[dateKey] = {
                high: item.main.temp,
                low: item.main.temp,
                icon: item.weather[0].icon,
                description: item.weather[0].description,
                day: date.toLocaleDateString('en-US', { weekday: 'short' })
            };
        } else {
            dailyForecasts[dateKey].high = Math.max(dailyForecasts[dateKey].high, item.main.temp);
            dailyForecasts[dateKey].low = Math.min(dailyForecasts[dateKey].low, item.main.temp);
        }
    });

    const forecastHTML = Object.entries(dailyForecasts)
        .slice(1, 4)
        .map(([_, data]) => `
            <div class="forecast-day">
                <div>${data.day}</div>
                <img src="${CONFIG.ICON_URL}/${data.icon}.png" alt="${data.description}">
                <div>H: ${Math.round(data.high)}°F</div>
                <div>L: ${Math.round(data.low)}°F</div>
            </div>
        `).join('');

    weatherBox.innerHTML = `
        <div class="weather-content">
            <div class="weather-header">
                <div class="location-temp">
                    <h3>North Canton, OH</h3>
                    <div class="current-weather">
                        <img src="${CONFIG.ICON_URL}/${current.weather[0].icon}@2x.png" alt="${current.weather[0].description}">
                        <div class="weather-info">
                            <p class="temp">${temp}°F</p>
                            <p class="description">${current.weather[0].description}</p>
                        </div>
                    </div>
                    <div class="weather-details">
                        <p>Feels like: ${Math.round(current.main.feels_like)}°F</p>
                        <p>Humidity: ${current.main.humidity}%</p>
                        <p>Wind: ${Math.round(current.wind.speed)} mph</p>
                    </div>
                </div>
                <div class="forecast-section">
                    <h4>3-Day Forecast</h4>
                    <div class="forecast-container">
                        ${forecastHTML}
                    </div>
                </div>
            </div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    getWeatherData();
    setInterval(getWeatherData, 900000);
});