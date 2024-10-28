import React from 'react';
import '../css/styles.css';

const PartnersList = ({ partners, onSelectPartner }) => {
  return (
    <div className="partners-list-container">
      <h3>Истории чатов</h3>
      <ul className="partners-list">
        {partners.length > 0 ? (
          partners.map((partner, index) => (
            <li key={index} onClick={() => onSelectPartner(partner)} className="partner-item">
              {partner}
            </li>
          ))
        ) : (
          <li className="no-partners">Нет истории</li>
        )}
      </ul>
    </div>
  );
};

export default PartnersList;


