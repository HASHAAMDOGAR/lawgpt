from sqlalchemy import (
    create_engine, Column, Integer, String, Date, Text, Boolean, Float, ForeignKey,
    Enum, DateTime, Table
)
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime

Base = declarative_base()

class CourtLevel(enum.Enum):
    supreme = "supreme"
    high = "high"
    district = "district"
    other = "other"

class PartyRole(enum.Enum):
    plaintiff = "plaintiff"
    respondent = "respondent"
    appellant = "appellant"
    defendant = "defendant"
    intervener = "intervener"

class IndividualRole(enum.Enum):
    judge = "judge"
    counsel = "counsel"
    witness = "witness"
    expert = "expert"

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class CaseRelationType(enum.Enum):
    applied = "applied"
    followed = "followed"
    distinguished = "distinguished"
    overruled = "overruled"
    affirmed = "affirmed"
    reversed = "reversed"

class DocumentType(enum.Enum):
    pdf = "pdf"
    transcript = "transcript"
    html = "html"
    scanned_image = "scanned_image"

class HearingType(enum.Enum):
    oral = "oral"
    written = "written"
    reserved = "reserved"

class OutcomeStatus(enum.Enum):
    affirmed = "affirmed"
    dismissed = "dismissed"
    remanded = "remanded"
    modified = "modified"
    not_set_aside = "not_set_aside"

class ProvisionType(enum.Enum):
    constitution = "constitution"
    statute = "statute"
    regulation = "regulation"
    rule = "rule"

class SectionType(enum.Enum):
    facts = "facts"
    issues = "issues"
    analysis = "analysis"
    ratio = "ratio"
    obiter = "obiter"
    conclusion = "conclusion"

class OpinionType(enum.Enum):
    majority = "majority"
    concurring = "concurring"
    dissenting = "dissenting"
    plurality = "plurality"

class LegalTopic(enum.Enum):
    contract = "contract"
    tort = "tort"
    criminal = "criminal"
    constitutional = "constitutional"
    administrative = "administrative"
    commercial = "commercial"
    family = "family"
    labour = "labour"
    tax = "tax"
    property = "property"

class Court(Base):
    __tablename__ = 'courts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Enum(CourtLevel))
    region = Column(String)
    parent_id = Column(Integer, ForeignKey('courts.id'), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    docket_number = Column(String)
    case_title = Column(String)
    filing_date = Column(Date)
    judgment_date = Column(Date)
    court_id = Column(Integer, ForeignKey('courts.id'))
    headnote = Column(Text)
    summary = Column(Text)
    conclusion = Column(Text)
    full_text = Column(Text)
    outcome = Column(Enum(OutcomeStatus))
    bench_size = Column(Integer)
    en_banc = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Judge(Base):
    __tablename__ = 'judges'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    background = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CaseJudge(Base):
    __tablename__ = 'case_judges'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    judge_id = Column(Integer, ForeignKey('judges.id'), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Party(Base):
    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    background = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Individual(Base):
    __tablename__ = 'individuals'
    id = Column(Integer, primary_key=True)
    actual_name = Column(String)
    masked_name = Column(String)
    gender = Column(Enum(Gender))
    is_minor = Column(Boolean)
    can_publish_name = Column(Boolean)
    mask_reason = Column(String)
    mask_timestamp = Column(DateTime)
    background = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Counsel(Base):
    __tablename__ = 'counsels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    firm = Column(String)
    background = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CaseParty(Base):
    __tablename__ = 'case_parties'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    party_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    role = Column(Enum(PartyRole))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseIndividual(Base):
    __tablename__ = 'case_individuals'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    individual_id = Column(Integer, ForeignKey('individuals.id'), primary_key=True)
    role = Column(Enum(IndividualRole))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CaseCounsel(Base):
    __tablename__ = 'case_counsels'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    counsel_id = Column(Integer, ForeignKey('counsels.id'), primary_key=True)
    representing_party = Column(Integer, ForeignKey('parties.id'))  # Optional reference
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Hearing(Base):
    __tablename__ = 'hearings'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    hearing_date = Column(Date)
    type = Column(Enum(HearingType))
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    type = Column(Enum(DocumentType))
    file_path = Column(String)
    file_size = Column(Integer)
    ocr_confidence = Column(Float)
    extracted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Footnote(Base):
    __tablename__ = 'footnotes'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    number = Column(Integer)
    location_ref = Column(String)
    text = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseEvent(Base):
    __tablename__ = 'case_events'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    event_date = Column(Date)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Citation(Base):
    __tablename__ = 'citations'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    cited_case_id = Column(Integer, ForeignKey('cases.id'))
    cited_case_title = Column(String)
    cited_case_reference = Column(String)
    relation_type = Column(Enum(CaseRelationType))
    binding = Column(Boolean)
    principle_summary = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseAppeal(Base):
    __tablename__ = 'case_appeals'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    appealed_to_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    appeal_level = Column(Enum(CourtLevel))
    appeal_date = Column(Date)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseCitationOrder(Base):
    __tablename__ = 'case_citation_order'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    jurisdiction_id = Column(Integer, ForeignKey('courts.id'), primary_key=True)
    priority = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Statute(Base):
    __tablename__ = 'statutes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    section = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class LegalProvision(Base):
    __tablename__ = 'legal_provisions'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(ProvisionType))
    name = Column(String)
    article = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseStatute(Base):
    __tablename__ = 'case_statutes'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    statute_id = Column(Integer, ForeignKey('statutes.id'), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseProvision(Base):
    __tablename__ = 'case_provisions'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    provision_id = Column(Integer, ForeignKey('legal_provisions.id'), primary_key=True)
    binding = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class InterpretivePrinciple(Base):
    __tablename__ = 'interpretive_principles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CasePrinciple(Base):
    __tablename__ = 'case_principles'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    principle_id = Column(Integer, ForeignKey('interpretive_principles.id'), primary_key=True)
    persuasive = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseTopic(Base):
    __tablename__ = 'case_topics'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    topic = Column(Enum(LegalTopic), primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseIssue(Base):
    __tablename__ = 'case_issues'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    issue_id = Column(Integer, ForeignKey('issues.id'), primary_key=True)
    weight = Column(Integer)

class CaseSection(Base):
    __tablename__ = 'case_sections'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    section_type = Column(Enum(SectionType))
    start_para = Column(Integer)
    end_para = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CasePanelOpinion(Base):
    __tablename__ = 'case_panel_opinions'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    judge_id = Column(Integer, ForeignKey('judges.id'), primary_key=True)
    opinion_type = Column(Enum(OpinionType))
    order_signed = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CaseCitationStats(Base):
    __tablename__ = 'case_citation_stats'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    cites_outgoing = Column(Integer)
    cites_incoming = Column(Integer)
    centrality_score = Column(Float)
    updated_at = Column(DateTime)

class CaseEmbedding(Base):
    __tablename__ = 'case_embeddings'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    vector = Column(String)  # Alternatively, use ARRAY(Float) if supported

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class CaseTag(Base):
    __tablename__ = 'case_tags'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class CaseKeyword(Base):
    __tablename__ = 'case_keywords'
    case_id = Column(Integer, ForeignKey('cases.id'), primary_key=True)
    keyword = Column(String, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)




