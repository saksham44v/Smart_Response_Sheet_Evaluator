document.addEventListener("DOMContentLoaded", () => {
            console.log("yaha tak phauvhe");
            // const data = {{ result | tojson }};  // Pass the result from Flask to JS

            //console.log(data);  // Check if it's available
    
            
            // document.getElementById("total-score").textContent = data.total_score;
            // console.log("reultsss")
            // document.getElementById("attempted").textContent = data.attempted;
            // document.getElementById("correct").textContent = data.correct;
            // document.getElementById("incorrect").textContent = data.incorrect;
            // document.getElementById("skipped").textContent = data.skipped;
            // document.getElementById("accuracy").textContent = data.accuracy;

            // document.getElementById("physics-score").textContent = data.physics.score;
            // document.getElementById("physics-attempted").textContent = data.physics.attempted;
            // document.getElementById("physics-correct").textContent = data.physics.correct;
            // document.getElementById("physics-incorrect").textContent = data.physics.incorrect;
            // document.getElementById("physics-accuracy").textContent = data.physics.accuracy;

            // document.getElementById("chemistry-score").textContent = data.chemistry.score;
            // document.getElementById("chemistry-attempted").textContent = data.chemistry.attempted;
            // document.getElementById("chemistry-correct").textContent = data.chemistry.correct;
            // document.getElementById("chemistry-incorrect").textContent = data.chemistry.incorrect;
            // document.getElementById("chemistry-accuracy").textContent = data.chemistry.accuracy;

            // document.getElementById("maths-score").textContent = data.maths.score;
            // document.getElementById("maths-attempted").textContent = data.maths.attempted;
            // document.getElementById("maths-correct").textContent = data.maths.correct;
            // document.getElementById("maths-incorrect").textContent = data.maths.incorrect;
            // document.getElementById("maths-accuracy").textContent = data.maths.accuracy;

            // Update progress bars
            document.getElementById("attempted-progress-bar").style.width = `${(data.attempted / 75) * 100}%`;
            document.getElementById("correct-progress-bar").style.width = `${(data.correct / 75) * 100}%`;
            document.getElementById("incorrect-progress-bar").style.width = `${(data.incorrect / 75) * 100}%`;
            document.getElementById("skipped-progress-bar").style.width = `${(data.skipped / 75) * 100}%`;
            document.getElementById("completed-progress-bar").style.width = `${data.completed_percentage}%`;
            document.getElementById("accuracy-progress-bar").style.width = `${data.accuracy}%`;
            
            /// Update subject-wise progress bars

// Physics
document.getElementById("physics-attempted-progress-bar").style.width = `${(data.subject_data.Physics.attempted / 25) * 100}%`;
document.getElementById("physics-correct-progress-bar").style.width = `${(data.subject_data.Physics.correct / data.subject_data.Physics.attempted) * 100}%`;
document.getElementById("physics-incorrect-progress-bar").style.width = `${(data.subject_data.Physics.incorrect / data.subject_data.Physics.attempted) * 100}%`;
document.getElementById("physics-accuracy-progress-bar").style.width = `${data.subject_data.Physics.accuracy}%`;

// Chemistry
document.getElementById("chemistry-attempted-progress-bar").style.width = `${(data.subject_data.Chemistry.attempted / 25)  * 100}%`;
document.getElementById("chemistry-correct-progress-bar").style.width = `${(data.subject_data.Chemistry.correct / data.subject_data.Chemistry.attempted) * 100}%`;
document.getElementById("chemistry-incorrect-progress-bar").style.width = `${(data.subject_data.Chemistry.incorrect / data.subject_data.Chemistry.attempted) * 100}%`;
document.getElementById("chemistry-accuracy-progress-bar").style.width = `${data.subject_data.Chemistry.accuracy}%`;

// Mathematics
document.getElementById("maths-attempted-progress-bar").style.width = `${(data.subject_data.Mathematics.attempted / 25) * 100}%`;
document.getElementById("maths-correct-progress-bar").style.width = `${(data.subject_data.Mathematics.correct / data.subject_data.Mathematics.attempted) * 100}%`;
document.getElementById("maths-incorrect-progress-bar").style.width = `${(data.subject_data.Mathematics.incorrect / data.subject_data.Mathematics.attempted) * 100}%`;
document.getElementById("maths-accuracy-progress-bar").style.width = `${data.subject_data.Mathematics.accuracy}%`;

           //circular progress 
           
           // Helper function to update circular progress
function updateCircularProgress(elementId, percentage) {
    const progressElement = document.getElementById(elementId);
    if (progressElement) {
        progressElement.style.background = `conic-gradient(#6366f1 ${percentage * 3.6}deg, #e5e7eb 0deg)`;
    }
}

// Update circular progress for Physics, Chemistry, Mathematics
updateCircularProgress("physics-progress", data.subject_data.Physics.score);
updateCircularProgress("chemistry-progress", data.subject_data.Chemistry.score);
updateCircularProgress("maths-progress", data.subject_data.Mathematics.score);


            //chem
            
            console.log(q);


            // const numberContainer = document.getElementById('number-container');
            // const dynamicContainer = document.getElementById('dynamic-container');
            
            // // Create number buttons
            // function displayNumbers() {
            //     for (let i = 1; i <= 75; i++) {
            //         const numberDiv = document.createElement('div');
            //         numberDiv.textContent = i;
            //         numberDiv.classList.add('cursor-pointer', 'px-3', 'py-2', 'bg-gray-200', 'rounded', 'hover:bg-gray-300');
            //         numberDiv.addEventListener('click', () => {
            //             // Remove active class from previous
            //             const activeNumber = document.querySelector('.active-number');
            //             if (activeNumber) {
            //                 activeNumber.classList.remove('active-number');
            //             }
            //             numberDiv.classList.add('active-number');
            
            //             // Clear old question display
            //             dynamicContainer.innerHTML = '';
            
            //             // Add new question display
            //             const questionElement = createQuestionDisplay(i);
            //             dynamicContainer.appendChild(questionElement);
            //         });
            //         numberContainer.appendChild(numberDiv);
            //     }
            // }
            
            // function createQuestionDisplay(i) {
            //     const mainContainer = document.createElement('div');
            //     mainContainer.style.display = 'flex';
            //     mainContainer.style.flexDirection = 'column';
            //     mainContainer.style.alignItems = 'center';
            //     mainContainer.style.gap = '20px';
            //     mainContainer.style.marginTop = '30px';
            //     mainContainer.style.padding = '20px';
            //     mainContainer.style.border = '1px solid #d1d5db';
            //     mainContainer.style.borderRadius = '8px';
            //     mainContainer.style.backgroundColor = '#f9fafb';
            //     mainContainer.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            
            //     const question = q[i - 1]; // 0-based indexing
            
            //     // Question Image
            //     if (question.question_image_url && question.question_image_url !== "None") {
            //         const questionImageDiv = document.createElement('div');
            //         questionImageDiv.style.display = 'flex';
            //         questionImageDiv.style.justifyContent = 'center';
            
            //         const questionImage = document.createElement('img');
            //         questionImage.src = "https://cdn3.digialm.com" + question.question_image_url;
            //         questionImage.alt = 'Question Image';
            //         questionImage.style.maxWidth = '100%';
            //         questionImage.style.maxHeight = '400px';
            //         questionImage.style.borderRadius = '8px';
            //         questionImage.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            
            //         questionImageDiv.appendChild(questionImage);
            //         mainContainer.appendChild(questionImageDiv);
            //     }
            
            //     // Options
            //     if (question.question_type === "SA") {
            //         // Subjective/Numerical Answer
            //         const answerDiv = document.createElement('div');
            //         answerDiv.style.marginTop = '20px';
            //         answerDiv.style.fontSize = '18px';
            //         answerDiv.style.color = '#1f2937';
            //         answerDiv.style.textAlign = 'center';
                    
            //         answerDiv.innerHTML = `
            //             <div><strong>Your Answer:</strong> ${question.given_answer}</div>
            //         `;
            
            //         mainContainer.appendChild(answerDiv);
            //     } else {
            //         // MCQ
            //         if (question.option_image_urls && question.option_image_urls[0] !== "None") {
            //             const optionsContainer = document.createElement('div');
            //             optionsContainer.style.display = 'flex';
            //             optionsContainer.style.flexDirection = 'column';  // 1 per row
            //             optionsContainer.style.gap = '16px';
            //             optionsContainer.style.marginTop = '20px';
            //             optionsContainer.style.width = '100%'; // full width
            
            //             question.option_image_urls.forEach((optionUrl, index) => {
            //                 if (optionUrl) {
            //                     const optionRow = document.createElement('div');
            //                     optionRow.style.display = 'flex';
            //                     optionRow.style.alignItems = 'center';
            //                     optionRow.style.gap = '10px';
            //                     optionRow.style.width = '100%';
            
            //                     // A, B, C, D text
            //                     const optionLabel = document.createElement('div');
            //                     optionLabel.textContent = String.fromCharCode(65 + index) + '.';
            //                     optionLabel.style.fontWeight = 'bold';
            //                     optionLabel.style.fontSize = '18px';
            //                     optionLabel.style.minWidth = '30px';
            //                     optionLabel.style.textAlign = 'right';
            
            //                     // Option Image
            //                     const optionImage = document.createElement('img');
            //                     optionImage.src = "https://cdn3.digialm.com" + optionUrl;
            //                     optionImage.alt = `Option ${String.fromCharCode(65 + index)}`; // A, B, C, D
            //                     optionImage.style.maxWidth = '100%';
            //                     optionImage.style.maxHeight = '150px';
            //                     optionImage.style.borderRadius = '6px';
            //                     optionImage.style.boxShadow = '0 1px 6px rgba(0,0,0,0.1)';
            //                     optionImage.style.flexGrow = '1';
            
            //                     optionRow.appendChild(optionLabel);
            //                     optionRow.appendChild(optionImage);
            //                     optionsContainer.appendChild(optionRow);
            //                 }
            //             });
            
            //             mainContainer.appendChild(optionsContainer);
            //         }
            //     }
            
            //     return mainContainer;
            // }
            
            
            // // Initial call
            // if (q && q.length > 0) {
            //     displayNumbers();
            // }


          
                const numberContainer = document.getElementById('number-container');
                const dynamicContainer = document.getElementById('dynamic-container');
                const correctAnswerKey =answer; // Make sure this is correctly defined
                //const q = [.../* Your question data array */ ]; // Make sure this is correctly defined
            
                // Create number buttons with color coding
                function displayNumbers() {
                    for (let i = 0; i < q.length; i++) { // Iterate through the question array
                        const questionData = q[i];
                        const numberDiv = document.createElement('div');
                        numberDiv.textContent = i + 1;
                        numberDiv.classList.add('cursor-pointer', 'flex', 'items-center', 'justify-center');
                        // Apply color based on status
                        if (questionData.status === 'Answered') {
                            const chosenOption = questionData.chosen_option;
                            const correctOption = correctAnswerKey[questionData.question_id];
            
                            if (chosenOption && correctOption && questionData.option_ids[Number(chosenOption)-1] === correctOption.toString()) {
                                numberDiv.classList.add('correct');
                            } else if (chosenOption && correctOption && questionData.option_ids[Number(chosenOption)-1] !== correctOption.toString()) {
                                numberDiv.classList.add('incorrect');
                            } else if (questionData.given_answer && correctAnswerKey[questionData.question_id] && questionData.given_answer.toString().trim() === correctAnswerKey[questionData.question_id].toString().trim()) {
                                numberDiv.classList.add('correct');
                            } else if (questionData.given_answer && correctAnswerKey[questionData.question_id] && questionData.given_answer.toString().trim() !== correctAnswerKey[questionData.question_id].toString().trim()) {
                                numberDiv.classList.add('incorrect');
                            }
            
                        } else if (questionData.status === 'Not Answered' || questionData.status === 'Skipped') {
                            numberDiv.classList.add('skipped');
                        }
                        numberDiv.addEventListener('click', () => {
                            const activeNumber = document.querySelector('.active-number');
                            if (activeNumber) {
                                activeNumber.classList.remove('active-number');
                            }
                            numberDiv.classList.add('active-number');
            
                            // Clear old question display
                            dynamicContainer.innerHTML = '';
            
                            // Add new question display
                            const questionElement = createQuestionDisplay(questionData, correctAnswerKey);
                            dynamicContainer.appendChild(questionElement);
                        });
                        numberContainer.appendChild(numberDiv);
                    }
                }



                function getVideoSolution(questionId) {
                    // In a real scenario, you would fetch the video URL based on the questionId
                    // from your backend or a data source.
                    // For example:
                    // return fetch(`/api/videos/${questionId}`).then(res => res.json()).then(data => data.url);
                    // Or, if you have a local map:
                    const videoMap = {
                        /* 'questionId1': 'url1.mp4', */
                        // Add your question ID to video URL mappings here
                    };
                    //return videoMap[questionId];
                    return 'static/solution.mp4';
                }
            
                function createQuestionDisplay(question, correctAnswers) {
                    const mainContainer = document.createElement('div');
                    mainContainer.innerHTML = `<h2>Question ${q.indexOf(question) + 1}</h2>`;



                    // ➕ Add Topic & Sub-topic tags if available
                  const topicInfo = topics[question.question_id];
                  if (topicInfo && topicInfo.topic && topicInfo.sub_topic) {
                      const tagContainer = document.createElement('div');
                      tagContainer.style.display = 'flex';
                      tagContainer.style.justifyContent = 'flex-end';
                      tagContainer.style.gap = '10px';
                      tagContainer.style.marginBottom = '10px';
              
                      const topicTag = document.createElement('span');
                      topicTag.textContent = topicInfo.topic;
                      topicTag.classList.add('tag-topic');
              
                      const subTopicTag = document.createElement('span');
                      subTopicTag.textContent = topicInfo.sub_topic;
                      subTopicTag.classList.add('tag-sub-topic');
              
                      tagContainer.appendChild(topicTag);
                      tagContainer.appendChild(subTopicTag);
                      mainContainer.appendChild(tagContainer);
                  }

            
                    // Question Image
                    if (question.question_image_url && question.question_image_url !== "None") {
                        const img = document.createElement('img');
                        img.src = "https://cdn3.digialm.com" + question.question_image_url;
                        img.alt = 'Question Image';
                        mainContainer.appendChild(img);
                    }
            
                    if (question.question_type === "SA") {
                        // Subjective/Numerical Answer
                        mainContainer.innerHTML += `<div><strong>Your Answer:</strong> ${question.given_answer !== '--' ? question.given_answer : '<span class="skipped-answer">Skipped</span>'}</div>`;
                        const correctAnswerSA = correctAnswers[question.question_id];
                        if (correctAnswerSA) {
                            mainContainer.innerHTML += `<div><strong>Correct Answer:</strong> ${correctAnswerSA}</div>`;
                        }
                    } else {
                        // MCQ
                        if (question.option_image_urls && question.option_image_urls[0] !== "None") {
                            const optionsContainer = document.createElement('div');
                            optionsContainer.classList.add('options-container');
            
                            question.option_image_urls.forEach((optionUrl, index) => {
                                if (optionUrl) {
                                    const optionRow = document.createElement('div');
                                    optionRow.classList.add('option-row');
                                    optionRow.innerHTML = `<span class="option-label">${String.fromCharCode(65 + index)}.</span><img src="https://cdn3.digialm.com${optionUrl}" alt="Option ${String.fromCharCode(65 + index)}">`;
                                    optionsContainer.appendChild(optionRow);
                                }
                            });
                            mainContainer.appendChild(optionsContainer);
                        }
            
                        const yourAnswerMCQ = question.chosen_option !== '--' ? String.fromCharCode(64 + parseInt(question.chosen_option)) : '<span class="skipped-answer">Skipped</span>';
                        const correctAnswerMCQ = correctAnswers[question.question_id] ? String.fromCharCode(65 + parseInt(question.option_ids.indexOf(correctAnswers[question.question_id])  )) : 'Not Available';
            
                        mainContainer.innerHTML += `<div class="your-answer"><strong>Your Answer:</strong> ${yourAnswerMCQ}</div>`;
                        mainContainer.innerHTML += `<div class="correct-answer"><strong>Correct Answer:</strong> ${correctAnswerMCQ}</div>`;
                    }

                    // Video Solution
                    const videoUrl = getVideoSolution(question.question_id); // Function to get video URL
                    if (videoUrl) {
                        const videoContainer = document.createElement('div');
                        videoContainer.style.marginTop = '20px';
                        videoContainer.innerHTML = `
                            <h3>Solution Video</h3>
                            <video width="100%" controls>
                                <source src="${videoUrl}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        `;
                        mainContainer.appendChild(videoContainer);
                    }
                
    
            
                    return mainContainer;
                }
            
                // Initial call
                if (q && q.length > 0 && correctAnswerKey) {
                    displayNumbers();
                    // Display the first question by default
                    const firstQuestionData = q[0];
                    if (firstQuestionData) {
                        const firstNumberDiv = numberContainer.firstChild;
                        if (firstNumberDiv) {
                            firstNumberDiv.classList.add('active-number');
                        }
                        dynamicContainer.appendChild(createQuestionDisplay(firstQuestionData, correctAnswerKey));
                    }
                }
           
            


      
});
