/// <reference types="Cypress" />

context('Add School', () => {
    beforeEach(() => {
        cy.visit('/');
        cy.get('#Login')
            .find('#inputEmail').type('user_1');
        cy.get('#Login')
            .find('#inputPassword').type('123456aA');
        cy.get('#Login')
            .submit();
    });

    // https://on.cypress.io/interacting-with-elements

    it('add school', () => {
        cy.get('#add_new_school')
            .click();

        cy.get('#register_school').should('exist');

        cy.get('#school_name')
            .type('my_school');

        cy.get("#submit_school")
            .click();

        cy.get('.alert-success')
            .should('exist');
    });
});
