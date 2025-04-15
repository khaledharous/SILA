document.addEventListener('DOMContentLoaded', function() {
    // Load data from localStorage if available
    const savedData = localStorage.getItem('studentRecords');
    let students = [];
    let columns = [];
    
    if (savedData) {
        const parsedData = JSON.parse(savedData);
        students = parsedData.students || [];
        columns = parsedData.columns || [
            { id: 'td', name: 'TD Mark' },
            { id: 'tp', name: 'TP Mark' },
            { id: 'controle', name: 'Contrôle Mark' }
        ];
    } else {
        // Default data
        students = [
            { name: 'Adam Smith' },
            { name: 'Alice Johnson' },
            { name: 'Benjamin Davis' }
        ];
        columns = [
            { id: 'td', name: 'TD Mark' },
            { id: 'tp', name: 'TP Mark' },
            { id: 'controle', name: 'Contrôle Mark' }
        ];
    }

    const dictionaryElement = document.getElementById('dictionary');
    const newItemInput = document.getElementById('newItem');
    const addButton = document.getElementById('addBtn');
    const newColumnInput = document.getElementById('newColumn');
    const addColumnBtn = document.getElementById('addColumnBtn');
    const saveButton = document.getElementById('saveBtn');

    // Get last name for sorting
    function getLastName(fullName) {
        return fullName.split(' ')[1] || fullName;
    }

    // Save data to localStorage
    function saveData() {
        const dataToSave = {
            students: students,
            columns: columns
        };
        localStorage.setItem('studentRecords', JSON.stringify(dataToSave));
        alert('Changes saved successfully!');
    }

    // Render the table
    function renderTable() {
        // Sort students by last name then first name
        students.sort((a, b) => {
            const aLast = getLastName(a.name);
            const bLast = getLastName(b.name);
            return aLast.localeCompare(bLast) || a.name.localeCompare(b.name);
        });

        dictionaryElement.innerHTML = '';

        const tableContainer = document.createElement('div');
        tableContainer.className = 'student-table-container';
        
        const table = document.createElement('table');
        table.className = 'student-table';
        
        // Table header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        // Action column
        const actionHeader = document.createElement('th');
        actionHeader.textContent = 'Actions';
        headerRow.appendChild(actionHeader);
        
        // Name column
        const nameHeader = document.createElement('th');
        nameHeader.textContent = 'Student Name';
        headerRow.appendChild(nameHeader);
        
        // Mark columns
        columns.forEach(col => {
            const colHeader = document.createElement('th');
            colHeader.textContent = col.name;
            
            if (!['td', 'tp', 'controle'].includes(col.id)) {
                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-column';
                removeBtn.textContent = '×';
                removeBtn.addEventListener('click', () => removeColumn(col.id));
                colHeader.appendChild(removeBtn);
            }
            
            headerRow.appendChild(colHeader);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Table body
        const tbody = document.createElement('tbody');
        
        students.forEach((student, index) => {
            const row = document.createElement('tr');
            
            // Delete button
            const actionCell = document.createElement('td');
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-student';
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', () => deleteStudent(index));
            actionCell.appendChild(deleteBtn);
            row.appendChild(actionCell);
            
            // Student name
            const nameCell = document.createElement('td');
            nameCell.textContent = student.name;
            row.appendChild(nameCell);
            
            // Mark inputs
            columns.forEach(col => {
                const markCell = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'mark-input';
                input.value = student[col.id] || '';
                input.placeholder = '0-20';
                input.min = '0';
                input.max = '20';
                input.addEventListener('change', () => {
                    student[col.id] = input.value;
                });
                
                // Clear button for marks
                const clearBtn = document.createElement('button');
                clearBtn.className = 'clear-mark';
                clearBtn.textContent = '×';
                clearBtn.addEventListener('click', () => {
                    input.value = '';
                    student[col.id] = '';
                });
                
                markCell.appendChild(input);
                markCell.appendChild(clearBtn);
                row.appendChild(markCell);
            });
            
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        tableContainer.appendChild(table);
        dictionaryElement.appendChild(tableContainer);
    }

    // Delete student
    function deleteStudent(index) {
        if (confirm('Are you sure you want to delete this student?')) {
            students.splice(index, 1);
            renderTable();
        }
    }

    // Add new student
    function addNewStudent() {
        const newStudentName = newItemInput.value.trim();
        if (newStudentName && !students.some(s => s.name === newStudentName)) {
            const newStudent = { name: newStudentName };
            columns.forEach(col => {
                newStudent[col.id] = '';
            });
            students.push(newStudent);
            renderTable();
            newItemInput.value = '';
        } else if (students.some(s => s.name === newStudentName)) {
            alert('Student already exists!');
        }
    }

    // Add new column
    function addNewColumn() {
        const newColumnName = newColumnInput.value.trim();
        if (newColumnName && !columns.some(c => c.name === newColumnName)) {
            const newColumnId = newColumnName.toLowerCase().replace(/\s+/g, '-');
            columns.push({
                id: newColumnId,
                name: newColumnName
            });
            
            students.forEach(student => {
                student[newColumnId] = '';
            });
            
            renderTable();
            newColumnInput.value = '';
        } else if (columns.some(c => c.name === newColumnName)) {
            alert('Column already exists!');
        }
    }

    // Remove column
    function removeColumn(columnId) {
        if (confirm('Are you sure you want to delete this column and all its data?')) {
            columns = columns.filter(col => col.id !== columnId);
            students.forEach(student => {
                delete student[columnId];
            });
            renderTable();
        }
    }

    // Event listeners
    addButton.addEventListener('click', addNewStudent);
    newItemInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') addNewStudent();
    });
    
    addColumnBtn.addEventListener('click', addNewColumn);
    newColumnInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') addNewColumn();
    });
    
    saveButton.addEventListener('click', saveData);

    // Initial render
    renderTable();
});