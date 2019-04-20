/// <reference types="Cypress" />

context('Login', () => {
    beforeEach(() => {
        cy.visit('/')
    });

    // https://on.cypress.io/interacting-with-elements

    it('submit- login the user', () => {
        cy.get('#Login')
            .find('#inputEmail').type('user_1');
        cy.get('#Login')
            .find('#inputPassword').type('123456aA');
        cy.get('#Login')
            .submit();
        cy.get('#navbarSupportedContent').should('exist');
    });
});
