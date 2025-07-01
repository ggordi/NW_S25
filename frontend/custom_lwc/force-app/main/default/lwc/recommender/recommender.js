import { LightningElement, track } from 'lwc';

export default class StockFilterForm extends LightningElement {
  @track form = {
    sector: '',
    marketCapLevel: '',
    growthValueType: '',
    forwardPE: ''
  };

  @track recommendation = ''; // for displaying the response text

  @track recommendations = ['AAPL', 'MSFT', 'GOOG'];

  get sectorOptions() {
    return [
      { label: 'Technology', value: 'Technology' },
      { label: 'Healthcare', value: 'Healthcare' },
      { label: 'Financial Services', value: 'Financial Services' },
      { label: 'Consumer Defensive', value: 'Consumer Defensive' },
      { label: 'Industrials', value: 'Industrials' },
      { label: 'Energy', value: 'Energy' }
    ];
  }

  get marketCapOptions() {
    return [
      { label: 'Low', value: 'Low' },
      { label: 'Medium', value: 'Medium' },
      { label: 'High', value: 'High' }
    ];
  }

  get growthValueOptions() {
    return [
      { label: 'Growth', value: 'Growth' },
      { label: 'Value', value: 'Value' }
    ];
  }

  handleChange(event) {
    const { name, value } = event.target;
    this.form = { ...this.form, [name]: value };
  }

  async handleSubmit() {
    console.log('Submitting:', this.form);

    try {
      const response = await fetch('https://your-api.com/recommendation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.form)
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json(); // or use await response.text() if it's plain text
      this.recommendation = data.message || JSON.stringify(data); // adjust based on response structure

    } catch (error) {
      console.error('Error:', error);
      this.recommendation = 'Something went wrong. Please try again.';
    }
  }
}
