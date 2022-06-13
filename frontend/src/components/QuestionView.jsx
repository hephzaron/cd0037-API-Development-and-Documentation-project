import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
    constructor() {
        super();
        this.state = {
            questions: [],
            page: 1,
            totalQuestions: 0,
            categories: {},
            currentCategory: null,
            search: false,
            searchResults: {}
        };
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions = () => {
        $.ajax({
            url: `/questions?page=${this.state.page}`, //TODO: update request URL
            type: 'GET',
            success: (result) => {
                this.setState({
                    search: false,
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    categories: result.categories,
                    currentCategory: result.current_category,
                });
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again');
                return;
            },
        });
    };

    selectPage(num) {
        this.setState({ page: num }, () => this.getQuestions());
    }

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / 10);
        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push( <span key = { i }
                className = { `page-num ${i === this.state.page ? 'active' : ''}` }
                onClick = {() => { this.selectPage(i); }} >
                { i }
                </span>);
            }
            return pageNumbers;
        }

    getByCategory = (id) => {
        $.ajax({
            url: `/categories/${id}/questions`, //TODO: update request URL
            type: 'GET',
            success: (result) => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,
                });
                return;
            },
            error: (error) => {
                alert('Unable to load questions. Please try your request again');
                return;
            },
        })
    };

    submitSearch = (searchTerm) => {
        $.ajax({
            url: `/questions`, //TODO: update request URL
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({ searchTerm: searchTerm }),
            xhrFields: {
                withCredentials: true,
            },
            crossDomain: true,
            success: (result) => {

                /*Get categories that returns the search item*/
                const categoriesWithSearchItem = Object.keys(result).filter(
                    key => result[`${key}`]['total_questions'] > 0
                )

                /*Enable JSX to render first category with search item*/
                let currentCategory = categoriesWithSearchItem[0]
                this.setState({
                    search: true,
                    searchResults: result,
                    questions: result[`${currentCategory}`].questions,
                    totalQuestions: result[`${currentCategory}`].total_questions
                });
                return;
            },
            error: (error) => {
                alert(error.responseJSON['message']);
                return;
            },
        })
    };

    questionAction = (id) => (action) => {
        if (action === 'DELETE') {
            if (window.confirm('are you sure you want to delete the question?')) {
                $.ajax({
                    url: `/questions/${id}`, //TODO: update request URL
                    type: 'DELETE',
                    success: (result) => {

                        /**Add: Update question list in state on delete */
                        let questions = this.state.questions.filter(
                            question => question.id !== result.id
                        )
                        this.setState({
                            questions: questions
                        })
                        return;

                    },
                    error: (error) => {
                        alert('Unable to load questions. Please try your request again');
                        return;
                    }
                });
            }
        }
    };

    render() {
        return ( <div className = 'question-view'>
                    <div className = 'categories-list'>
                        <h2 onClick = {() => {this.getQuestions();}}>
                        Categories
                        </h2>
                        <ul>{Object.keys(this.state.categories).map((id) => (
                            <li key = { id } onClick = {() => {
                                if (this.state.search) {
                                    let searchResults = this.state.searchResults[id]
                                    this.setState({
                                        questions: searchResults['questions'],
                                        totalQuestions: searchResults['total_questions'],
                                        currentCategory: searchResults['current_category']
                                    });
                                } else {
                                    this.getByCategory(id);
                                }}}>
                                {this.state.search &&
                                (<span className='numOfSearchItems'>{this.state.searchResults[id]['total_questions']}</span>)}
                                { this.state.categories[id] }
                                <img className = 'category'
                                alt = { `${this.state.categories[id].toLowerCase()}` }
                                src = { `${this.state.categories[id].toLowerCase()}.svg` }/>
                            </li>)
                            )}
                        </ul>
                        <Search submitSearch = { this.submitSearch }
                        getQuestions = { this.getQuestions }
                        search = { this.state.search }/>
                    </div>
                    <div className = 'questions-list' >
                        <h2> Questions </h2>
                        {this.state.questions.map((q, ind) => ( <Question key = { q.id }
                        question = { q.question }
                        answer = { q.answer }
                        category = { this.state.categories[q.category] }
                        difficulty = { q.difficulty }
                        questionAction = { this.questionAction(q.id) }/>
                        ))}
                        <div className = 'pagination-menu' > { this.createPagination() } </div>
                    </div>
                </div>
            );
        }
    }

export default QuestionView;