BEGIN TRANSACTION;
CREATE TABLE categories (
	VariableID integer NOT NULL,
	DataValue double NOT NULL,
	CategoryDescription text NOT NULL
);
CREATE TABLE censorcodecv (
	Term varchar(50) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE datatypecv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE datavalues (
	ValueID integer NOT NULL,
	DataValue double NOT NULL,
	ValueAccuracy double,
	LocalDateTime varchar(50) NOT NULL,
	UTCOffset double NOT NULL,
	DateTimeUTC varchar(50) NOT NULL,
	SiteID integer NOT NULL,
	VariableID integer NOT NULL,
	OffsetValue double,
	OffsetTypeID integer,
	CensorCode varchar(50) NOT NULL,
	QualifierID integer,
	MethodID integer NOT NULL,
	SourceID integer NOT NULL,
	SampleID integer,
	DerivedFromID integer,
	QualityControlLevelID integer NOT NULL,
	PRIMARY KEY (ValueID)
);
CREATE TABLE derivedfrom (
	DerivedFromID integer NOT NULL,
	ValueID integer NOT NULL
);
CREATE TABLE generalcategorycv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE groupdescriptions (
	GroupID integer NOT NULL,
	GroupDescription text,
	PRIMARY KEY (GroupID)
);
CREATE TABLE groups (
	GroupID integer NOT NULL,
	ValueID integer NOT NULL
);
CREATE TABLE isometadata (
	MetadataID integer NOT NULL,
	TopicCategory varchar(255) NOT NULL,
	Title varchar(255) NOT NULL,
	Abstract text NOT NULL,
	ProfileVersion varchar(255) NOT NULL,
	MetadataLink text,
	PRIMARY KEY (MetadataID)
);
CREATE TABLE labmethods (
	LabMethodID integer NOT NULL,
	LabName varchar(255) NOT NULL,
	LabOrganization varchar(255) NOT NULL,
	LabMethodName varchar(255) NOT NULL,
	LabMethodDescription text NOT NULL,
	LabMethodLink text,
	PRIMARY KEY (LabMethodID)
);
CREATE TABLE methods (
	MethodID integer NOT NULL,
	MethodDescription text NOT NULL,
	MethodLink text,
	PRIMARY KEY (MethodID)
);
CREATE TABLE odmversion (
	VersionNumber varchar(50) NOT NULL
);
CREATE TABLE offsettypes (
	OffsetTypeID integer NOT NULL,
	OffsetUnitsID integer NOT NULL,
	OffsetDescription text NOT NULL,
	PRIMARY KEY (OffsetTypeID)
);
CREATE TABLE qualifiers (
	QualifierID integer NOT NULL,
	QualifierCode varchar(50),
	QualifierDescription text NOT NULL,
	PRIMARY KEY (QualifierID)
);
CREATE TABLE qualitycontrollevels (
	QualityControlLevelID integer NOT NULL,
	QualityControlLevelCode varchar(50) NOT NULL,
	Definition varchar(255) NOT NULL,
	Explanation text NOT NULL,
	PRIMARY KEY (QualityControlLevelID)
);
CREATE TABLE samplemediumcv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE samples (
	SampleID integer NOT NULL,
	SampleType varchar(255) NOT NULL,
	LabSampleCode varchar(50) NOT NULL,
	LabMethodID integer NOT NULL,
	PRIMARY KEY (SampleID)
);
CREATE TABLE sampletypecv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE seriescatalog (
	SeriesID integer NOT NULL,
	SiteID integer,
	SiteCode varchar(50),
	SiteName varchar(255),
	SiteType varchar(255),
	VariableID integer,
	VariableCode varchar(50),
	VariableName varchar(255),
	Speciation varchar(255),
	VariableUnitsID integer,
	VariableUnitsName varchar(255),
	SampleMedium varchar(255),
	ValueType varchar(255),
	TimeSupport double,
	TimeUnitsID integer,
	TimeUnitsName varchar(255),
	DataType varchar(255),
	GeneralCategory varchar(255),
	MethodID integer,
	MethodDescription text,
	SourceID integer,
	Organization varchar(255),
	SourceDescription text,
	Citation text,
	QualityControlLevelID integer,
	QualityControlLevelCode varchar(50),
	BeginDateTime varchar(50),
	EndDateTime varchar(50),
	BeginDateTimeUTC varchar(50),
	EndDateTimeUTC varchar(50),
	ValueCount integer,
	PRIMARY KEY (SeriesID)
);
CREATE TABLE sites (
	SiteID integer NOT NULL,
	SiteCode varchar(50) NOT NULL,
	SiteName varchar(255) NOT NULL,
	Latitude double NOT NULL,
	Longitude double NOT NULL,
	LatLongDatumID integer NOT NULL,
	SiteType varchar(255),
	Elevation_m double,
	VerticalDatum varchar(255),
	LocalX double,
	LocalY double,
	LocalProjectionID integer,
	PosAccuracy_m double,
	State varchar(255),
	County varchar(255),
	Comments text,
	PRIMARY KEY (SiteID)
);
CREATE TABLE sitetypecv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE sources (
	SourceID integer NOT NULL,
	Organization varchar(255) NOT NULL,
	SourceDescription text NOT NULL,
	SourceLink text,
	ContactName varchar(255) NOT NULL,
	Phone varchar(255) NOT NULL,
	Email varchar(255) NOT NULL,
	Address varchar(255) NOT NULL,
	City varchar(255) NOT NULL,
	State varchar(255) NOT NULL,
	ZipCode varchar(255) NOT NULL,
	Citation text NOT NULL,
	MetadataID integer NOT NULL,
	PRIMARY KEY (SourceID)
);
CREATE TABLE spatialreferences (
	SpatialReferenceID integer NOT NULL,
	SRSID integer,
	SRSName varchar(255) NOT NULL,
	IsGeographic integer,
	Notes text,
	PRIMARY KEY (SpatialReferenceID)
);
CREATE TABLE speciationcv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE topiccategorycv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE units (
	UnitsID integer NOT NULL,
	UnitsName varchar(255) NOT NULL,
	UnitsType varchar(255) NOT NULL,
	UnitsAbbreviation varchar(255) NOT NULL,
	PRIMARY KEY (UnitsID)
);
CREATE TABLE valuetypecv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE variablenamecv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
CREATE TABLE variables (
	VariableID integer NOT NULL,
	VariableCode varchar(50) NOT NULL,
	VariableName varchar(255) NOT NULL,
	Speciation varchar(255) NOT NULL,
	VariableUnitsID integer NOT NULL,
	SampleMedium varchar(255) NOT NULL,
	ValueType varchar(255) NOT NULL,
	IsRegular integer NOT NULL,
	TimeSupport double NOT NULL,
	TimeUnitsID integer NOT NULL,
	DataType varchar(255) NOT NULL,
	GeneralCategory varchar(255) NOT NULL,
	NoDataValue double NOT NULL,
	PRIMARY KEY (VariableID)
);
CREATE TABLE verticaldatumcv (
	Term varchar(255) NOT NULL,
	Definition text,
	PRIMARY KEY (Term)
);
ALTER TABLE categories
	ADD FOREIGN KEY (VariableID) 
	REFERENCES variables (VariableID);


ALTER TABLE datavalues
	ADD FOREIGN KEY (QualityControlLevelID) 
	REFERENCES qualitycontrollevels (QualityControlLevelID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (QualifierID) 
	REFERENCES qualifiers (QualifierID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (VariableID) 
	REFERENCES variables (VariableID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (OffsetTypeID) 
	REFERENCES offsettypes (OffsetTypeID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (SourceID) 
	REFERENCES sources (SourceID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (MethodID) 
	REFERENCES methods (MethodID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (SiteID) 
	REFERENCES sites (SiteID);

ALTER TABLE datavalues
	ADD FOREIGN KEY (CensorCode) 
	REFERENCES censorcodecv (Term);

ALTER TABLE datavalues
	ADD FOREIGN KEY (SampleID) 
	REFERENCES samples (SampleID);


ALTER TABLE derivedfrom
	ADD FOREIGN KEY (ValueID) 
	REFERENCES datavalues (ValueID);


ALTER TABLE groups
	ADD FOREIGN KEY (ValueID) 
	REFERENCES datavalues (ValueID);

ALTER TABLE groups
	ADD FOREIGN KEY (GroupID) 
	REFERENCES groupdescriptions (GroupID);


ALTER TABLE isometadata
	ADD FOREIGN KEY (TopicCategory) 
	REFERENCES topiccategorycv (Term);


ALTER TABLE offsettypes
	ADD FOREIGN KEY (OffsetUnitsID) 
	REFERENCES units (UnitsID);


ALTER TABLE samples
	ADD FOREIGN KEY (SampleType) 
	REFERENCES sampletypecv (Term);

ALTER TABLE samples
	ADD FOREIGN KEY (LabMethodID) 
	REFERENCES labmethods (LabMethodID);


ALTER TABLE sites
	ADD FOREIGN KEY (VerticalDatum) 
	REFERENCES verticaldatumcv (Term);

ALTER TABLE sites
	ADD FOREIGN KEY (LocalProjectionID,LatLongDatumID) 
	REFERENCES spatialreferences (SpatialReferenceID,SpatialReferenceID);

ALTER TABLE sites
	ADD FOREIGN KEY (SiteType) 
	REFERENCES sitetypecv (Term);


ALTER TABLE sources
	ADD FOREIGN KEY (MetadataID) 
	REFERENCES isometadata (MetadataID);


ALTER TABLE variables
	ADD FOREIGN KEY (Speciation) 
	REFERENCES speciationcv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (SampleMedium) 
	REFERENCES samplemediumcv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (VariableName) 
	REFERENCES variablenamecv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (GeneralCategory) 
	REFERENCES generalcategorycv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (ValueType) 
	REFERENCES valuetypecv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (DataType) 
	REFERENCES datatypecv (Term);

ALTER TABLE variables
	ADD FOREIGN KEY (TimeUnitsID,VariableUnitsID) 
	REFERENCES units (UnitsID,UnitsID);

