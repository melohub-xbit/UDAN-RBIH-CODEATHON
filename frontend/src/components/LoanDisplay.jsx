import React, { useState } from 'react';
import styled from 'styled-components';

const Container = styled.div`
  background: linear-gradient(to right, #2563eb, #1d4ed8);
  min-height: 100vh;
  padding: 2rem;
  color: #fff;
`;

const Grid = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.2);

  &:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.15);
    border-color: #fbbf24;
  }
`;

const Title = styled.h2`
  color: #fbbf24;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
`;

const DetailsList = styled.ul`
  list-style: none;
  padding: 0;
`;

const DetailItem = styled.li`
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #e5e7eb;
`;

const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  padding: 2rem;
  border-radius: 15px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const CloseButton = styled.button`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #fbbf24;
  font-size: 1.5rem;
  cursor: pointer;
`;

const Header = styled.div`
  text-align: center;
  padding: 2rem 0;
  max-width: 800px;
  margin: 0 auto;
`;

const LoanDisplay = ({ loans }) => {
  const [selectedLoan, setSelectedLoan] = useState(null);

  return (
    <Container>
      <Header>
        <h1 className="text-5xl font-extrabold text-white mb-6 leading-tight">
          Explore Our <span className="text-yellow-400">Loan Schemes</span>
        </h1>
        <p className="text-xl text-blue-100 mb-8">
          Find the perfect loan scheme tailored to your needs with our comprehensive selection of financial solutions.
        </p>
      </Header>
      
      <Grid>
        {loans.map((loan, index) => (
          <Card key={index} onClick={() => setSelectedLoan(loan)}>
            <Title>{loan.scheme}</Title>
            <DetailsList>
              <DetailItem>
                <strong>Target Group:</strong> {loan.target_group}
              </DetailItem>
              <DetailItem>
                <strong>Purpose:</strong>{' '}
                {Array.isArray(loan.purpose) ? loan.purpose[0] : loan.purpose}
              </DetailItem>
            </DetailsList>
          </Card>
        ))}
      </Grid>

      {selectedLoan && (
        <Modal onClick={() => setSelectedLoan(null)}>
          <ModalContent onClick={(e) => e.stopPropagation()}>
            <CloseButton onClick={() => setSelectedLoan(null)}>×</CloseButton>
            <Title>{selectedLoan.scheme}</Title>
            <DetailsList>
              <DetailItem>
                <strong>Target Group:</strong> {selectedLoan.target_group}
              </DetailItem>
              <DetailItem>
                <strong>Purpose:</strong>
                {Array.isArray(selectedLoan.purpose) ? (
                  <ul className="list-disc pl-4 mt-2">
                    {selectedLoan.purpose.map((p, i) => (
                      <li key={i} className="mb-1">{p}</li>
                    ))}
                  </ul>
                ) : (
                  selectedLoan.purpose
                )}
              </DetailItem>
              <DetailItem>
                <strong>Required Documents:</strong>
                <ul className="list-disc pl-4 mt-2">
                  {selectedLoan.documents.map((doc, i) => (
                    <li key={i} className="mb-1">{doc}</li>
                  ))}
                </ul>
              </DetailItem>
            </DetailsList>
          </ModalContent>
        </Modal>
      )}
    </Container>
  );
};

export default LoanDisplay;
