import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormView extends Component {
    constructor(props) {
        super();
        this.state = {
            question: '',
            answer: '',
            difficulty: 1,
            category: 1,
            rating: 1,
            categories: {},
        };
    }

    componentDidMount() {
        $.ajax({
            url: `/categories`, //TODO: update request URL
            type: 'GET',
            success: (result) => {
                this.setState({ categories: result.categories });
                return;
            },
            error: (error) => {
                alert('Unable to load categories. Please try your request again');
                return;
            },
        });
    }

    submitQuestion = (event) => {
        event.preventDefault();
        /**
         * Format user entry to add a Question mark if ommitted by user
         */
        const re = new RegExp('\\?$')
        let question = re.test(this.state.question) ? this.state.question : this.state.question.concat(' ?')
        $.ajax({
            url: '/questions', //TODO: update request URL
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                question: question,
                answer: this.state.answer,
                difficulty: this.state.difficulty,
                category: this.state.category,
                rating: this.state.rating
            }),
            xhrFields: {
                withCredentials: true,
            },
            crossDomain: true,
            success: (result) => {
                alert(result['message']);
                document.getElementById('add-question-form').reset();
                return;
            },
            error: (error) => {
                alert('Unable to add question. Please try your request again');
                return;
            },
        });
    };

    handleChange = (event) => {
        this.setState({
            [event.target.name]: event.target.value
        });
    };

    render() {
        return (
            <div id = 'add-form' >
                <h2 > Add a New Trivia Question </h2>
                <form className = 'form-view'
                id = 'add-question-form'
                onSubmit = { this.submitQuestion } >
                    <label>
                        Question
                        <input type = 'text'name = 'question' onChange = { this.handleChange }/>
                    </label >
                    <label>
                        Answer
                        <input type = 'text' name = 'answer' onChange = { this.handleChange }/>
                    </label>
                    <label>
                        Difficulty
                        <select name = 'difficulty' onChange = { this.handleChange }>
                            <option value = '1' > 1 </option>
                            <option value = '2' > 2 </option>
                            <option value = '3' > 3 </option>
                            <option value = '4' > 4 </option>
                            <option value = '5' > 5 </option>
                        </select >
                    </label>
                    <label>
                        Rating
                        <select name = 'rating' onChange = { this.handleChange }>
                            <option value = '1' > 1 </option>
                            <option value = '2' > 2 </option>
                            <option value = '3' > 3 </option>
                            <option value = '4' > 4 </option>
                            <option value = '5' > 5 </option>
                        </select >
                    </label>
                    <label>
                        Category
                        <select name = 'category' onChange = { this.handleChange } >
                        {
                        Object.keys(this.state.categories).map((id) => {
                            return ( <option key = { id } value = { id } > { this.state.categories[id] }
                            </option>);
                            })
                            }
                        </select>
                    </label>
                <input type = 'submit' className = 'button' value = 'Submit' />
            </form>
        </div>
        );
    }
}

export default FormView;