async function fetchExchangeRate() {
    const response = await fetch('/ferreteria/exchange_rate_view/');
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log("Datos de la API:", data);
    return data;
}

document.addEventListener('DOMContentLoaded', () => {
    const currencySelector = document.getElementById('currency-selector');
    const priceElement = document.querySelector('.price'); 
    const priceConvertedElement = document.getElementById('price-converted'); 

    fetchExchangeRate().then(data => {
        function updatePrices() {
            const selectedCurrency = currencySelector.value.toLowerCase();
            console.log("Moneda seleccionada:", selectedCurrency);
            const exchangeRate = data[selectedCurrency];
            console.log(`Datos de la moneda seleccionada (${selectedCurrency}):`, exchangeRate);
            
            if (exchangeRate) {
                console.log("Tasa de cambio para " + selectedCurrency.toUpperCase() + ": " + exchangeRate);

                const amountCLP = parseFloat(priceElement.dataset.amountClp);
                console.log("Cantidad en CLP:", amountCLP);

                if (!isNaN(amountCLP) && !isNaN(exchangeRate)) {
                    const convertedAmount = amountCLP / exchangeRate;
                    priceConvertedElement.textContent = `${selectedCurrency.toUpperCase()} ${convertedAmount.toFixed(2)}`;
                } else {
                    console.error('Datos no válidos para la conversión');
                    priceConvertedElement.textContent = 'Datos no válidos para la conversión';
                }
            } else {
                console.error(`No se encontró el valor de la tasa de cambio para ${selectedCurrency.toUpperCase()}`);
                priceConvertedElement.textContent = 'Tasa de cambio no disponible';
            }
        }

        updatePrices();  
        currencySelector.addEventListener('change', updatePrices);  
    }).catch(error => {
        console.error("Error fetching exchange rate:", error);
        priceConvertedElement.textContent = 'Error al cargar la tasa de cambio'; 
    });
});
